import os

"""
Returns the .JSON/.CSV data file path for a given repository.
Args:
    repo_name: str - The name of the repository.
    file_type: str - The file type, defaults to "json".
Returns:
    str - The data file path, e.g. "./data/restaurants.json".
"""
def get_repo_data_path(repo_name: str, file_type: str = "json") -> str:
    data_dir = os.getenv("DATA_DIR", os.getcwd())
    return os.path.join(data_dir, f"{repo_name}.{file_type}")
