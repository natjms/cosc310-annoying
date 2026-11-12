import os
from pathlib import Path


DATA_DIRECTORY_ENVIRONMENT_VARIABLE = "DATA_DIR"


def get_repository_data_file_path(filename: str, data_directory_path: Path | None = None) -> Path:
    """Returns the data file path for the given repository filename.

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
    path_string = os.getenv(DATA_DIRECTORY_ENVIRONMENT_VARIABLE)

    if not path_string:
        raise ValueError(
            f"A data directory path must be in .env under the key {environment_variable}."
        )

    return Path(path_string)
