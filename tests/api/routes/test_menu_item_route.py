from fastapi.testclient import TestClient
import pytest
from app import app
from ulid import ULID

from app.services import restaurant as restaurant_service
from app.services import menu as menu_service
from app.services import user as user_service
from app.services import menu_item as menu_item_service

client = TestClient(app)

@pytest.fixture
def test_data():
    user = user_service.create_user()
    restaurant = restaurant_service.create_restaurant(user.id, 'Test Restaurant')
    menu = menu_service.create_menu(restaurant.id, 'Test Menu')
    menu_item = menu_item_service.create_menu_item(
        restaurant.id,
        menu.id,
        'Test Menu Item',
        5.00
    )

    yield (user, restaurant, menu, menu_item)

    menu_service.delete_menu(restaurant.id, menu.id)
    restaurant_service.delete_restaurant(restaurant.id)
    user_service.delete_user(user.id)

def test_create_and_retrieve_single_menu_item(test_data):
    (_, restaurant, menu, _) = test_data

    response = client.post(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items',
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Test Item',
            'price': 5.00
        }
    )
    created_menu_item = response.json()

    assert response.status_code == 201

    response = client.get(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items/{created_menu_item["id"]}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Test Item'

def test_create_with_missing_data(test_data):
    (_, restaurant, menu, _) = test_data
    response = client.post(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items',
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Test Item',
        }
    )

    assert response.status_code == 422

def test_retrieve_all_missing_restaurant_returns_404(test_data):
    (_, _, menu, _) = test_data

    response = client.get(f'/api/restaurants/{ULID()}/menus/{menu.id}/items')
    assert response.status_code == 404

def test_retrieve_all_missing_menu_returns_404(test_data):
    (_, restaurant, _, menu_item) = test_data

    response = client.get(f'/api/restaurants/{restaurant.id}/menus/{ULID()}/items/{menu_item.id}')
    assert response.status_code == 404

def test_retrieve_single_missing_restaurant_returns_404(test_data):
    (_, _, menu, menu_item) = test_data

    response = client.get(f'/api/restaurants/{ULID()}/menus/{menu.id}/items/{menu_item.id}')
    assert response.status_code == 404

def test_retrieve_single_missing_menu_returns_404(test_data):
    (_, restaurant, _, menu_item) = test_data

    response = client.get(f'/api/restaurants/{restaurant.id}/menus/{ULID()}/items')
    assert response.status_code == 404

def test_update_menu_item(test_data):
    (_, restaurant, menu, menu_item) = test_data

    update_response = client.patch(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items/{menu_item.id}',
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'New title',
        }
    )

    assert update_response.status_code == 200

    response = client.get(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items/{menu_item.id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'New title'

def test_update_menu_item_with_invalid_price(test_data):
    (_, restaurant, menu, menu_item) = test_data

    update_response = client.patch(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items/{menu_item.id}',
        headers={'Content-Type': 'application/json'},
        json={
            'price': -5.00,
        }
    )

    assert update_response.status_code == 422

def test_update_menu_item_with_empty_string_is_idempotent(test_data):
    (_, restaurant, menu, menu_item) = test_data

    update_response = client.patch(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items/{menu_item.id}',
        headers={'Content-Type': 'application/json'},
        json={
            'name': '',
        }
    )

    assert update_response.status_code == 200

    retrieve_response = client.get(f'/api/restaurants/{restaurant.id}/menus/{menu.id}/items/{menu_item.id}')
    assert retrieve_response.json()['name'] == menu_item.name
