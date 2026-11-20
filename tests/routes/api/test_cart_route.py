import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app import app
from app.models.user import User
from app.repositories.restaurant import restaurants as restaurant_repo
from app.repositories.user import users as user_repo
from app.routes.api.cart import get_current_user
from app.services import restaurant as restaurant_service
from app.services import user as user_service

client = TestClient(app)

# BYPASSED AUTH
def override_get_current_user():
    return User(id=ULID(), username="test", email="test@test.com", password_hash=b"")

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", "password")
    restaurant = restaurant_service.create_restaurant(user.id, "Test Restaurant")
    yield (user, restaurant)
    restaurant_repo.delete(id=restaurant.id)
    user_repo.delete(id=user.id)

def test_add_negative_quantity_fails(test_data):
    _, restaurant = test_data
    response = client.patch(
        f"/api/carts/{restaurant.id}",
        params={"menu_item_id": str(ULID()), "quantity": -5},
    )
    assert response.status_code in [400, 422]

    get_response = client.get(f"/api/carts/{restaurant.id}")
    if get_response.status_code == 200:
        assert get_response.json()["items"] == {}

def test_clear_cart(test_data):
    _, restaurant = test_data
    response = client.delete(f"/api/carts/{restaurant.id}")
    assert response.status_code in [200, 204, 404]