""" import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app import app
from app.models.user import User
from app.repositories.restaurant import restaurants as restaurant_repo
from app.repositories.user import users as user_repo
from app.services import menu as menu_service
from app.services import menu_item as menu_item_service
from app.services import restaurant as restaurant_service
from app.services import user as user_service
from app.services import session as session_service

client = TestClient(app)

# "AVeryStr0ngPassw0rd!" hashed
password_hash = b"$2b$12$fuwt7LndvSSufxkgphaaEeLMD4/idE1ULAP2hqoOTWB9L2clq0DHO"

@pytest.fixture
def test_data():
    user = user_service.register_user('test', 'test@example.com', 'password', dangerously_set_password_hash=password_hash, role='customer')
    session = session_service.log_in('test', 'AVeryStr0ngPassw0rd!')
    restaurant = restaurant_service.create_restaurant(user.id, "Test Restaurant")
    menu = menu_service.create_menu(str(restaurant.id), "Test Menu")
    menu_item = menu_item_service.create_menu_item(str(menu.id), "Test Item", 5.00)

    yield (user, restaurant, menu_item, session)

    menu_service.delete_menu(restaurant.id, menu.id)
    restaurant_repo.delete(id=restaurant.id)
    user_repo.delete(id=user.id)


def test_add_item_and_get_cart(test_data):
    (_, restaurant, menu_item, session) = test_data

    response = client.patch(
        f"/api/carts/{restaurant.id}",
        headers={'Content-Type': 'application/json', 'X-Token': session.token},
        params={"menu_item_id": str(menu_item.id), "quantity": 2},
    )
    print(response.json())
    assert response.status_code == 200

    get_response = client.get(
        f"/api/carts/{restaurant.id}",
        headers={'Content-Type': 'application/json', 'X-Token': session.token}
    )
    assert get_response.status_code == 200

    cart_data = get_response.json()
    assert str(menu_item.id) in cart_data["items"]
    assert cart_data["items"][str(menu_item.id)]["quantity"] == 2


def test_add_negative_quantity_fails(test_data):
    (_, restaurant, menu_item, session) = test_data

    response = client.patch(
        f"/api/carts/{restaurant.id}",
        headers={'Content-Type': 'application/json', 'X-Token': session.token},
        params={"menu_item_id": str(menu_item.id), "quantity": -5},
    )
    assert response.status_code in [400, 422]

    get_response = client.get(
        f"/api/carts/{restaurant.id}",
        headers={'Content-Type': 'application/json', 'X-Token': session.token}
    )
    if get_response.status_code == 200:
        assert get_response.json()["items"] == {}


def test_clear_cart(test_data):
    (_, restaurant, menu_item, session) = test_data

    client.patch(
        f"/api/carts/{restaurant.id}",
        headers={'Content-Type': 'application/json', 'X-Token': session.token},
        params={"menu_item_id": str(menu_item.id), "quantity": 1},
    )
    response = client.delete(f"/api/carts/{restaurant.id}")
    assert response.status_code in [200, 204]

    get_response = client.get(
        f"/api/carts/{restaurant.id}",
        headers={'Content-Type': 'application/json', 'X-Token': session.token}
    )
    if get_response.status_code == 200:
        assert get_response.json()["items"] == {}
 """
