import os
import subprocess
import sys
from functions._paths import resolve_within


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """
    Runs a Python file within the working directory and returns its output.

    Args:
        working_directory (str): The base working directory.
        file_path (str): The path to the Python file to run.
        args (list[str] | None): Extra command-line arguments for the script.

    Returns:
        str: The script's output or an error message.
    """
    try:
        # Resolve the path and check it is within the working directory
        target_file = resolve_within(working_directory, file_path)
        if target_file is None:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Only allow Python files
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command, using the same interpreter that is running this code
        command = [sys.executable, target_file]
        if args:
            command.extend(args)

        # Run the script from the working directory, capturing its output as text
        result = subprocess.run(
            command,
            cwd=os.path.realpath(working_directory),
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Build the output string from the completed process
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)

    except Exception as e:
        # Catch any unexpected errors and return an error message
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory with optional command-line arguments, returning its stdout, stderr and exit code",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
