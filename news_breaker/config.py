import os

PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))


def get_project_path(path: str) -> str:
    """
    Get the absolute path of a file in the project.

    Args:
        path: path relative to the project root.
    Returns:
        Absolute path of the file.
    """
    return os.path.join(PROJECT_DIR, path)


def get_src_path(path: str) -> str:
    """
    Get the absolute path of a file in the project.

    Args:
        path: path relative to the project root.
    Returns:
        Absolute path of the file.
    """
    return os.path.join(SRC_DIR, path)
