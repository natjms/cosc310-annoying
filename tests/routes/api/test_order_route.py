""" import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app import app
from app.models.user import User
from app.routes.api.order import get_current_user
from app.services import cart as cart_service
from app.services import menu as menu_service
from app.services import menu_item as menu_item_service
from app.services import restaurant as restaurant_service
from app.services import user as user_service

client = TestClient(app)


# OVERRIDE !!!!!!!!!!!!!!!!!!
def override_get_current_user():
    return User(id=ULID(), username="test", email="test@test.com", password_hash=b"")


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", "password")
    restaurant = restaurant_service.create_restaurant(user.id, "Test Restaurant")
    menu = menu_service.create_menu(restaurant.id, "Test Menu")
    menu_item = menu_item_service.create_menu_item(str(menu.id), "Test Menu Item", 5.00)

    cart_service.add_item_to_cart(user.id, restaurant.id, menu.id, menu_item.id, 2)
    yield (user, restaurant, menu, menu_item)

    menu_service.delete_menu(restaurant.id, menu.id)
    restaurant_service.delete_restaurant(str(restaurant.id))
    user_service.delete_user(user.id)


def test_checkout(test_data):
    (_, restaurant, _, _) = test_data

    # rough outline of post
    response = client.post(
        f"/api/orders/?restaurant-id={restaurant.id}",
        headers={"Content-Type": "application/json"},
        json={"name": "Test Item", "price": 5.00},
    )
    assert response.status_code in [200, 201]
    assert response.json()["price"] == 20.00

    # this one intends to check if order history (persistence) works
    historical_response = client.get("/api/orders/")
    assert historical_response.status_code == 200
    assert len(historical_response.json()) > 0
 """
