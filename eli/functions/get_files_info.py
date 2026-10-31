import os
from functions._paths import resolve_within


def get_files_info(working_directory: str, directory: str) -> str:
    """
    Validates the target directory and ensures it is within the working directory.
    If valid, lists the contents of the directory.

    Args:
        working_directory (str): The base working directory.
        directory (str): The target directory to validate.

    Returns:
        str: Directory contents or an error message.
    """
    try:
        # Resolve the path and check it is within the working directory
        target_dir = resolve_within(working_directory, directory)
        if target_dir is None:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the target directory is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Build one line per entry; a failing entry is reported inline instead of aborting the listing
        entries = []
        for name in sorted(os.listdir(target_dir)):
            full_path = os.path.join(target_dir, name)
            try:
                size = os.path.getsize(full_path)
                is_dir = os.path.isdir(full_path)
                entries.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
            except OSError as e:
                entries.append(f"- {name}: Error: {e}")

        return "\n".join(entries)

    except Exception as e:
        # Catch any unexpected errors and return an error message
        return f'Error: {str(e)}'


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
