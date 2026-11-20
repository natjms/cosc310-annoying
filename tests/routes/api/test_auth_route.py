from fastapi import status
from fastapi.testclient import TestClient
from ulid import ULID
import pytest
from app import app

from app.exceptions import AuthenticationException
from app.repositories import users as user_repo, sessions as session_repo
from app.services import user as user_service, session as session_service

# "AVeryStr0ngPassw0rd!" hashed
password_hash = b"$2b$12$fuwt7LndvSSufxkgphaaEeLMD4/idE1ULAP2hqoOTWB9L2clq0DHO"

client = TestClient(app)
@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", "ignored parameter", dangerously_set_password_hash=password_hash)

    yield (user,)

    user_repo.delete_all()
    session_repo.delete_all()

@pytest.mark.parametrize("credentials", [
    ("test", "AVeryStr0ngPassw0rd!"),
    ("test@example.com", "AVeryStr0ngPassw0rd!")
])
def test_login_successful(test_data, credentials):
    (identifier, password) = credentials
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/json"},
        json={
            "username_or_email": identifier,
            "password_plaintext": password
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()

@pytest.mark.parametrize("credentials", [
    ("test", "incorrect password"),
    ("incorrect_username", "AVeryStr0ngPassw0rd!"),
    ("incorrect_username", "incorrect password")
])
def test_login_fails_with_incorrect_credentials(test_data, credentials):
    (identifier, password) = credentials
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/json"},
        json={
            "username_or_email": identifier,
            "password_plaintext": password
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.parametrize("payload", [
    {"username_or_email": "test"},
    {"password_plaintext": "AVeryStr0ngPassw0rd!"}
])
def test_login_fails_with_insufficient_credentials(payload):
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/json"},
        json=payload
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_logout_successfully(test_data):
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/json"},
        json={
            "username_or_email": "test",
            "password_plaintext": "AVeryStr0ngPassw0rd!"
        }
    )

    session = response.json()

    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {session['token']}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert not session_service.session_is_valid(session["token"])

def test_cannot_logout_with_non_existant_session():
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer faketoken"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
