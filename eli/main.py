import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {
        "role": "user",
        "content": args.user_prompt,
    }
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)


if response.usage is None:
    raise RuntimeError("No usage information returned from the API - the request may have failed.")

if args.verbose:
    print("User prompt: " + str(messages[0]["content"]))
    print("Prompt tokens: " + str(response.usage.prompt_tokens)) 
    print("Response tokens: " + str(response.usage.completion_tokens))

print("Response:") 
print(response.choices[0].message.content)

