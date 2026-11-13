import pytest

from app.services import user as user_service, session as session_service
from app.repositories import users as user_repository, sessions as session_repository
from app.exceptions import MissingValueException, AuthenticationException

@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", "password")

    yield (user,)

    user_repository.delete_all()
    session_repository.delete_all()

def test_log_in_succeeds_with_username(test_data):
    (user,) = test_data
    session = session_service.log_in(user.username, "password")
    assert session.user_id == user.id

def test_log_in_succeeds_with_email(test_data):
    (user,) = test_data
    session = session_service.log_in(user.email, "password")
    assert session.user_id == user.id

def test_log_in_with_invalid_account_raises():
    with pytest.raises(MissingValueException):
        session_service.log_in("fake_user", "password")

def test_log_in_with_invalid_password_raises(test_data):
    (user,) = test_data
    with pytest.raises(AuthenticationException):
        session_service.log_in(user.email, "invalid_password")

def test_log_out_succeeds(test_data):
    (user,) = test_data
    session = session_service.log_in(user.username, "password")
    session_service.log_out(session.token)

    with pytest.raises(MissingValueException):
       session_service.find_session(session.token)

def test_log_out_fails_for_fake_session():
    with pytest.raises(MissingValueException):
        session_service.log_out("fakesessiontoken")
