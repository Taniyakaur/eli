import json
from collections.abc import Callable

from config import WORKING_DIR
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_call, verbose: bool = False) -> dict:
    """
    Calls the function the LLM asked for and wraps its result in a tool message.

    Args:
        tool_call: One tool-call object from message.tool_calls.
        verbose (bool): Whether to print the arguments as well as the function name.

    Returns:
        dict: A "tool" role message holding the function's result, ready to append to messages.
    """
    function_name = tool_call.function.name or ""

    def tool_message(content: str) -> dict:
        return {"role": "tool", "tool_call_id": tool_call.id, "content": content}

    # The LLM sends its arguments as a JSON string; a malformed one is reported back instead of crashing
    try:
        function_args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError as e:
        return tool_message(f"Error: Invalid JSON arguments for {function_name}: {e}")
    if not isinstance(function_args, dict):
        return tool_message(f"Error: Arguments for {function_name} must be a JSON object")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function = function_map.get(function_name)
    if function is None:
        return tool_message(f"Error: Unknown function: {function_name}")

    # get_files_info has no default for directory, but the schema lets the LLM leave it out
    if function_name == "get_files_info":
        function_args.setdefault("directory", ".")

    # The working directory is injected here so the LLM can never choose or change it
    function_args["working_directory"] = WORKING_DIR

    try:
        result = function(**function_args)
    except TypeError as e:
        return tool_message(f"Error: Invalid arguments for {function_name}: {e}")

    return tool_message(result)
