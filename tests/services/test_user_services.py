import pytest

from app.services import user as user_service
from app.repositories.user import users as user_repository
from app.exceptions import MissingValueException, ResourceConflictException

@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", 'password')

    yield (user,)

    user_repository.delete_all()

def test_register_and_retrieve_user(test_data):
    user = user_service.register_user(username="test2", email="test2@example.com", password_plaintext="password")
    assert user_service.find_user_by_username("test2").id == user.id
    assert user_service.find_user_by_email("test2@example.com").id == user.id
    assert user_service.find_user_by_id(user.id).username == user.username

def test_attempt_to_register_duplicate_username_raises(test_data):
    with pytest.raises(ResourceConflictException):
        user = user_service.register_user(username="test", email="test2@example.com", password_plaintext="password")

def test_validate_credentials_with_invalid_account_raises():
    with pytest.raises(MissingValueException):
        user_service.validate_credentials("non_existant_account", "password")

def test_validate_credentials_with_incorrect_password_fails(test_data):
    (user,) = test_data
    assert user_service.validate_credentials(user.username, "incorrect_password") is False

def test_validate_credentials_with_password_succeeds(test_data):
    (user,) = test_data
    assert user_service.validate_credentials(user.username, "password")
