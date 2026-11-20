import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app import app
from app.models.user import User
from app.repositories.restaurant import restaurants as restaurant_repo
from app.repositories.user import users as user_repo
from app.routes.api.cart import get_current_user
from app.services import menu as menu_service
from app.services import restaurant as restaurant_service
from app.services import user as user_service

client = TestClient(app)


@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", "password")
    restaurant = restaurant_service.create_restaurant(user.id, "Test Restaurant")

    yield (user, restaurant)

    restaurant_repo.delete(id=restaurant.id)
    user_repo.delete(id=user.id)


def test_add_negative_quantity_fails(test_restaurant_id):
    response = client.patch(
        f"/api/carts/{test_restaurant_id}",
        params={"menu_item_id": str(ULID()), "quantity": -5},
    )
    assert response.status_code in [400, 422]

    get_response = client.get(f"/api/carts/{test_restaurant_id}")
    if get_response.status_code == 200:
        assert get_response.json()["items"] == {}


def test_clear_cart(test_restaurant_id):
    response = client.delete(f"/api/carts/{test_restaurant_id}")
    assert response.status_code in [200, 404]
