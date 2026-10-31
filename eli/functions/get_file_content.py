import os
from config import MAX_CHARS  # Import the character limit from config.py
from functions._paths import resolve_within


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Reads the content of a file if it is within the working directory.

    Args:
        working_directory (str): The base working directory.
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file or an error message.
    """
    try:
        # Resolve the path and check it is within the working directory
        target_file = resolve_within(working_directory, file_path)
        if target_file is None:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content up to MAX_CHARS
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)

            # Check if the file was truncated
            if f.read(1):  # Try to read one more character
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        # Catch any unexpected errors and return an error message
        return f'Error: {str(e)}'


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the text contents of a file relative to the working directory, truncating very long files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
