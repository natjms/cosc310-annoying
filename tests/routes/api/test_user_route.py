import pytest
from fastapi import status
from fastapi.testclient import TestClient
from ulid import ULID

from app import app
from app.exceptions import AuthenticationException
from app.repositories import sessions as session_repo
from app.repositories import users as user_repo
from app.services import role as role_service
from app.services import session as session_service
from app.services import user as user_service

# "AVeryStr0ngPassw0rd!" hashed
password_hash = b"$2b$12$fuwt7LndvSSufxkgphaaEeLMD4/idE1ULAP2hqoOTWB9L2clq0DHO"

client = TestClient(app)


@pytest.fixture
def test_data():
    user = user_service.register_user(
        "test",
        "test@example.com",
        "password",
        dangerously_set_password_hash=password_hash,
    )
    session = session_service.log_in("test", "AVeryStr0ngPassw0rd!")

    admin = user_service.register_user(
        "admin",
        "admin@example.com",
        "password",
        dangerously_set_password_hash=password_hash,
    )
    role_service.assign_role(admin.id, "admin")
    admin_session = session_service.log_in("admin", "AVeryStr0ngPassw0rd!")

    yield (user, session, admin_session)

    user_repo.delete_all()
    session_repo.delete_all()


CORRECT_REGISTER_PAYLOAD = {
    "username": "test2",
    "email": "test2@example.com",
    "password_plaintext": "AVeryStr0ngPassw0rd!",
}


def test_register_and_retrieve_success(test_data):
    response = client.post(
        "/api/users/",
        headers={"Content-Type": "application/json"},
        json=CORRECT_REGISTER_PAYLOAD,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "test2"

    user_id = response.json()["id"]

    session = session_service.log_in(
        response.json()["username"], "AVeryStr0ngPassw0rd!"
    )
    retrieve_response = client.get(
        f"/api/users/{user_id}", headers={"X-Token": session.token}
    )
    assert retrieve_response.status_code == status.HTTP_200_OK
    assert retrieve_response.json()["id"] == user_id


@pytest.mark.parametrize(
    "payload",
    [
        # Missing required data
        {"email": "test2@example.com", "password_plaintext": "AVeryStr0ngPassw0rd!"},
        {"username": "test2", "password_plaintext": "AVeryStr0ngPassw0rd!"},
        {"username": "test2", "email": "test2@example.com"},
        {**CORRECT_REGISTER_PAYLOAD, "username": "This is an invalid username"},
        {**CORRECT_REGISTER_PAYLOAD, "email": "This is an invalid email"},
        {**CORRECT_REGISTER_PAYLOAD, "password_plaintext": "weak"},
    ],
)
def test_validation_errors_in_user_registration(test_data, payload):
    response = client.post(
        "/api/users/", headers={"Content-Type": "application/json"}, json=payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_cant_register_duplicate_email(test_data):
    (user, *_) = test_data
    response = client.post(
        "/api/users/",
        headers={"Content-Type": "application/json"},
        json={**CORRECT_REGISTER_PAYLOAD, "email": user.email},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_cant_register_duplicate_username(test_data):
    (user, *_) = test_data
    response = client.post(
        "/api/users/",
        headers={"Content-Type": "application/json"},
        json={**CORRECT_REGISTER_PAYLOAD, "username": user.username},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_retrieve_user_without_session_fails(test_data):
    (user, *_) = test_data
    response = client.get(f"/api/users/{user.id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_retrieve_someone_elses_user_fails(test_data):
    (_, session, *_) = test_data

    response = client.post(
        "/api/users/",
        headers={"Content-Type": "application/json"},
        json=CORRECT_REGISTER_PAYLOAD,
    )

    response = client.get(
        f"/api/users/{response.json()['id']}", headers={"X-Token": session.token}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_missing_user_fails(test_data):
    (_, _, admin_session, *_) = test_data
    response = client.get(
        f"/api/users/{ULID()}", headers={"X-Token": admin_session.token}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_admin_can_retrieve_others(test_data):
    (user, _, admin_session) = test_data
    response = client.get(
        f"/api/users/{user.id}", headers={"X-Token": admin_session.token}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user.id


@pytest.mark.parametrize(
    "payload",
    [{"username": "updated_username"}, {"email": "updated_email@example.com"}],
)
def test_update_user_successfully(test_data, payload):
    (user, session, *_) = test_data

    response = client.patch(
        f"/api/users/{user.id}",
        headers={"Content-Type": "application/json", "X-Token": session.token},
        json=payload,
    )

    updated_field = list(payload.keys())[0]

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[updated_field] == payload[updated_field]


@pytest.mark.parametrize(
    "payload",
    [
        {"username": "This is an invalid username"},
        {"email": "This is an invalid email"},
        {"password_plaintext": "weak"},
    ],
)
def test_update_user_with_invalid_payload(test_data, payload):
    (user, session, *_) = test_data

    response = client.patch(
        f"/api/users/{user.id}",
        headers={"Content-Type": "application/json", "X-Token": session.token},
        json=payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_password_successfully(test_data):
    (user, session, *_) = test_data

    response = client.patch(
        f"/api/users/{user.id}",
        headers={"Content-Type": "application/json", "X-Token": session.token},
        json={"password_plaintext": "AVeryStr0ngPassw0rd!Updated"},
    )

    assert response.status_code == status.HTTP_200_OK

    with pytest.raises(AuthenticationException):
        session_service.log_in(user.username, "AVeryStr0ngPassw0rd!")

    session_service.log_in(user.username, "AVeryStr0ngPassw0rd!Updated")


def test_deactivate_account(test_data):
    (user, session, *_) = test_data
    response = client.delete(
        f"/api/users/{user.id}", headers={"X-Token": session.token}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(AuthenticationException):
        session_service.log_in(user.username, "AVeryStr0ngPassw0rd!")


def test_deactivate_someone_elses_account_fails(test_data):
    (user, session, *_) = test_data

    response = client.post(
        "/api/users/",
        headers={"Content-Type": "application/json"},
        json=CORRECT_REGISTER_PAYLOAD,
    )

    response = client.delete(
        f"/api/users/{response.json()['id']}", headers={"X-Token": session.token}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_deactivate_someones_account_as_admin(test_data):
    (user, session, admin_session) = test_data
    response = client.delete(
        f"/api/users/{user.id}", headers={"X-Token": admin_session.token}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(AuthenticationException):
        session_service.log_in(user.username, "AVeryStr0ngPassw0rd!")


def test_cannot_deactivate_non_existant_account(test_data):
    (_, _, admin_session) = test_data
    response = client.delete(
        f"/api/users/{ULID()}", headers={"X-Token": admin_session.token}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
