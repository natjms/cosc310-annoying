import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app import app
from app.exceptions import MissingValueException
from app.repositories.restaurant import restaurants as restaurant_repo
from app.repositories.user import users as user_repo
from app.services import restaurant as restaurant_service
from app.services import session as session_service
from app.services import user as user_service

client = TestClient(app)

# "AVeryStr0ngPassw0rd!" hashed
password_hash = b"$2b$12$fuwt7LndvSSufxkgphaaEeLMD4/idE1ULAP2hqoOTWB9L2clq0DHO"


@pytest.fixture
def test_data():
    user = user_service.register_user(
        "test",
        "test@example.com",
        "password",
        dangerously_set_password_hash=password_hash,
        role="restaurateur",
    )
    session = session_service.log_in("test", "AVeryStr0ngPassw0rd!")
    restaurant = restaurant_service.create_restaurant(user.id, "Test Restaurant")

    yield (user, restaurant, session)

    restaurant_repo.delete(id=restaurant.id)
    user_repo.delete(id=user.id)


def test_cannot_get_nonexistant_restaurant():
    response = client.get(f"/api/restaurants/{ULID()}")
    assert response.status_code == 404


def test_create_and_retrieve_restaurant(test_data):
    (user, _, session) = test_data

    create_response = client.post(
        "/api/restaurants/",
        headers={"Content-Type": "application/json", "X-Token": session.token},
        json={
            "owner_id": str(user.id),
            "name": "Created Restaurant",
        },
    )

    assert create_response.status_code == 201
    new_restaurant_id = create_response.json()["id"]

    retrieve_response = client.get(f"/api/restaurants/{new_restaurant_id}")
    assert retrieve_response.json()["name"] == "Created Restaurant"

    restaurant_repo.delete(id=ULID.from_str(new_restaurant_id))


def test_attempt_to_create_restaurant_with_fake_user(test_data):
    (_, _, session) = test_data
    create_response = client.post(
        "/api/restaurants/",
        headers={"Content-Type": "application/json", "X-Token": session.token},
        json={
            "owner_id": str(ULID()),
            "name": "Created Restaurant",
        },
    )

    assert create_response.status_code == 404


def test_update_restaurant(test_data):
    (_, restaurant, session) = test_data

    update_response = client.patch(
        f"/api/restaurants/{restaurant.id}",
        headers={"Content-Type": "application/json", "X-Token": session.token},
        json={"name": "Updated Restaurant"},
    )

    assert update_response.status_code == 200

    retrieve_response = client.get(f"/api/restaurants/{restaurant.id}")
    assert retrieve_response.json()["name"] == "Updated Restaurant"
