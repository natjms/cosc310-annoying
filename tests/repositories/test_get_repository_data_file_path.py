import pytest

from app.repositories.utils import get_repository_data_file_path, DATA_DIRECTORY_ENVIRONMENT_VARIABLE
FILENAME = "restaurants.json"


# Typical

def test_from_env(monkeypatch, tmp_path):
    temporary_path_string  = str(tmp_path)
    monkeypatch.setenv(DATA_DIRECTORY_ENVIRONMENT_VARIABLE, temporary_path_string)

    path = get_repository_data_file_path(FILENAME)

    expected_path = tmp_path / FILENAME

    assert path == expected_path


# Extreme

def test_explicit_directory(tmp_path):
    explicit_directory_path = tmp_path

    path = get_repository_data_file_path(FILENAME, explicit_directory_path)

    expected_path = explicit_directory_path / FILENAME

    assert path == expected_path


# Erroneous

def test_missing_env_variable(monkeypatch):
    monkeypatch.delenv(DATA_DIRECTORY_ENVIRONMENT_VARIABLE, raising=False)

    with pytest.raises(ValueError):
        get_repository_data_file_path(FILENAME)


def test_empty_env_variable(monkeypatch):
    monkeypatch.setenv(DATA_DIRECTORY_ENVIRONMENT_VARIABLE, "")

    with pytest.raises(ValueError):
        get_repository_data_file_path(FILENAME)
