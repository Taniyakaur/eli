import os
from config import MAX_CHARS  # Import the character limit from config.py


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
        # Ensure the working directory is an absolute path
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the file is within the working directory
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
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