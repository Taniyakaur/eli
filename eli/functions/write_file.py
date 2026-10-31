import os
from functions._paths import resolve_within


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Writes content to a file within the working directory.

    Args:
        working_directory (str): The base working directory.
        file_path (str): The path to the file to write.
        content (str): The content to write to the file.

    Returns:
        str: Success or error message.
    """
    try:
        # Resolve the path and check it is within the working directory
        target_file = resolve_within(working_directory, file_path)
        if target_file is None:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the file_path points to an existing directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure all parent directories exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Write the content to the file
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        # Catch any unexpected errors and return an error message
        return f'Error: {str(e)}'


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory, creating the file (and parent directories) if needed or overwriting it if it exists",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
