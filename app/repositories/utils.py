import os
from pathlib import Path

DATA_DIRECTORY_ENVIRONMENT_VARIABLE = "DATA_DIR"


def get_repository_data_file_path(
    filename: str, data_directory_path: Path | None = None
) -> Path:
    """
    Returns the data file path for the given repository filename.

    Args:
        filename: The name of the repository data file (e.g., "restaurants.json").
        data_directory_path: Optional override for the base directory. Defaults to the path specified at the environment variable DATA_DIR and if that is not present, raise a ValueError.
    """

    if not data_directory_path:
        data_directory_path = _get_environment_data_directory_path(
            DATA_DIRECTORY_ENVIRONMENT_VARIABLE
        )

    return data_directory_path / filename


def _get_environment_data_directory_path(environment_variable: str) -> Path:
    path_string = os.getenv(environment_variable)

    if path_string is None:
        raise ValueError(
            f"data directory is not configured! please set {environment_variable} in .env "
            f"tip: you can do this by either copying example.env to .env or passing data_directory_path explicitly."
        )
    return Path(path_string)
