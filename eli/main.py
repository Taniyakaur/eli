import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI
import argparse

from prompts import system_prompt
from call_function import available_functions, call_function

MAX_ITERATIONS = 20  # Stops the agent from looping forever and burning tokens


def main() -> None:
    load_dotenv(override=True)
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")
    if api_key != api_key.strip().strip("\"'"):
        raise RuntimeError("OPENROUTER_API_KEY has extra spaces or quote marks around it - check your .env file")
    if not api_key.startswith("sk-or-"):
        raise RuntimeError("OPENROUTER_API_KEY doesn't look like an OpenRouter key (they start with 'sk-or-')")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="eli: a command-line coding agent")
    parser.add_argument("user_prompt", type=str, help="Task for the agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print("User prompt: " + args.user_prompt)

    # Keep calling the model until it stops asking for tools and gives a final answer
    for _ in range(MAX_ITERATIONS):
        message = generate_content(client, messages, args.verbose)

        if not message.tool_calls:
            if message.content is None:
                raise RuntimeError("The model returned no text content.")
            print("Response:")
            print(message.content)
            return

        # The assistant's tool-call request must be in the history before the matching tool results
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [tool_call.model_dump() for tool_call in message.tool_calls],
        })
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Function {tool_call.function.name} returned no content")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    print(f"Error: Agent did not finish within {MAX_ITERATIONS} iterations", file=sys.stderr)
    sys.exit(1)


def generate_content(client: OpenAI, messages: list[dict], verbose: bool):
    """
    Sends the conversation to the model and returns its reply message.

    Args:
        client (OpenAI): The OpenRouter client.
        messages (list[dict]): The conversation so far.
        verbose (bool): Whether to print token usage.

    Returns:
        The model's reply message, which may contain text and/or tool calls.
    """
    # Free models often fail with transient provider errors (e.g. 504 timeouts), so retry a few times
    for attempt in range(1, 4):
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=messages,
            tools=available_functions,
        )
        if response.choices:
            break
        print(f"Provider error on attempt {attempt}: {getattr(response, 'error', None)}", file=sys.stderr)
        time.sleep(2 * attempt)
    else:
        raise RuntimeError(f"The model returned no choices (likely a temporary provider error): {getattr(response, 'error', None)}")

    if verbose and response.usage is not None:
        print("Prompt tokens: " + str(response.usage.prompt_tokens))
        print("Response tokens: " + str(response.usage.completion_tokens))

    return response.choices[0].message

if __name__ == "__main__":
    main()
