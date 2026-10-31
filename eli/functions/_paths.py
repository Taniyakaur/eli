import os


def resolve_within(working_directory: str, path: str) -> str | None:
    """
    Resolves path relative to working_directory, following symlinks.

    Returns:
        str | None: The resolved absolute path, or None if it falls outside the working directory.
    """
    working_dir_abs = os.path.realpath(working_directory)
    target = os.path.realpath(os.path.join(working_dir_abs, path))
    if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
        return None
    return target
