from fastapi.testclient import TestClient
import pytest
from app import app
from ulid import ULID

from app.services import restaurant as restaurant_service
from app.services import menu as menu_service
from app.services import user as user_service
from app.services import session as session_service

client = TestClient(app)

# "AVeryStr0ngPassw0rd!" hashed
password_hash = b"$2b$12$fuwt7LndvSSufxkgphaaEeLMD4/idE1ULAP2hqoOTWB9L2clq0DHO"

@pytest.fixture
def test_data():
    user = user_service.register_user('test', 'test@example.com', 'password', dangerously_set_password_hash=password_hash, role='restaurateur')
    session = session_service.log_in(user.username, 'AVeryStr0ngPassw0rd!')
    restaurant = restaurant_service.create_restaurant(user.id, 'Test Restaurant')
    menu = menu_service.create_menu(restaurant.id, 'Test Menu')

    yield (user, restaurant, menu, session)

    menu_service.delete_menu(menu.id)
    restaurant_service.delete_restaurant(restaurant.id)
    user_service.delete_user(user.id)

def test_create_and_retrieve_menu(test_data):
    (_, restaurant, menu, session) = test_data

    response = client.post(f'/api/menus/',
        headers={'Content-Type': 'application/json', 'X-Token': session.token},
        json={
            'restaurant_id': str(restaurant.id),
            'name': 'Test Menu',
        }
    )

    assert response.status_code == 201

    created_menu = response.json()
    response = client.get(f'/api/menus/{created_menu["id"]}')
