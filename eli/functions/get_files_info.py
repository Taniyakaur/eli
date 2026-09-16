import os

def get_files_info(working_directory, directory):
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
        # Ensure the working directory is an absolute path
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Check if the target directory is within the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the target directory is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Iterate over the items in the target directory and build the output
        entries = []
        for name in os.listdir(target_dir):
            full_path = os.path.join(target_dir, name)
            try:
                size = os.path.getsize(full_path)
                is_dir = os.path.isdir(full_path)
                entries.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                return f'Error: Failed to process "{name}" - {str(e)}'

        # Return the formatted directory contents
        return "\n".join(entries)

    except Exception as e:
        # Catch any unexpected errors and return an error message
        return f'Error: {str(e)}'