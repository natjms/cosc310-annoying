from ulid import ULID
import pytest
import math

from app.exceptions import MissingValueException
from app.services import menu_item as menu_item_service
from app.services import restaurant as restaurant_service
from app.services import menu as menu_service
from app.services import user as user_service

from app.repositories import menu

@pytest.fixture
def test_data():
    user = user_service.create_user()
    restaurant = restaurant_service.create_restaurant(user.id, 'Test Restaurant')
    menu = menu_service.create_menu(restaurant.id, 'Test Menu')

    yield (user, restaurant, menu)

    menu_service.delete_menu(restaurant.id, menu.id)
    restaurant_service.delete_restaurant(restaurant.id)
    user_service.delete_user(user.id)

def test_get_menu_item_raises_for_nonexistant_restaurant_fails(test_data):
    (_, restaurant, menu) = test_data
    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    with pytest.raises(MissingValueException):
        menu_item_service.get_menu_item_by_id(ULID(), menu.id, created_menu_item.id)

def test_get_menu_item_raises_for_nonexistant_menu_fails(test_data):
    (_, restaurant, menu) = test_data
    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    with pytest.raises(MissingValueException):
        menu_item_service.get_menu_item_by_id(restaurant.id, ULID(), created_menu_item.id)

def test_create_menu_item_and_get_by_id(test_data):
    (_, restaurant, menu) = test_data

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    retrieved_menu_item = menu_item_service.get_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id)

    assert created_menu_item.id == retrieved_menu_item.id
    assert created_menu_item.name == retrieved_menu_item.name
    assert math.isclose(created_menu_item.price, retrieved_menu_item.price)

def test_cannot_get_menu_item_that_doesnt_exist(test_data):
    (_, restaurant, menu) = test_data
    with pytest.raises(MissingValueException):
        menu_item_service.get_menu_item_by_id(restaurant.id, menu.id, ULID())

def test_get_all_menu_items_actually_adds_items(test_data):
    (_, restaurant, menu) = test_data

    all_menu_items = menu_item_service.get_all_menu_items(restaurant.id, menu.id)

    assert len(all_menu_items) == 0

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    all_menu_items = menu_item_service.get_all_menu_items(restaurant.id, menu.id)

    assert len(all_menu_items) == 1
    assert all_menu_items[0].name == 'Test Item'

def test_cannot_update_nonexistant_menu_item(test_data):
    (_, restaurant, menu) = test_data
    with pytest.raises(MissingValueException):
        menu_item_service.update_menu_item_by_id(restaurant.id, menu.id, ULID(), {})

def test_cannot_update_menu_item_if_restaurant_doesnt_exist(test_data):
    (_, restaurant, menu) = test_data
    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    with pytest.raises(MissingValueException):
        menu_item_service.update_menu_item_by_id(ULID(), menu.id, created_menu_item.id, {})

def test_cannot_update_menu_item_if_menu_doesnt_exist(test_data):
    (_, restaurant, menu) = test_data
    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    with pytest.raises(MissingValueException):
        menu_item_service.update_menu_item_by_id(restaurant.id, ULID(), created_menu_item.id, {})

def test_update_menu_item_price(test_data):
    (_, restaurant, menu) = test_data

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    updated_menu_item = menu_item_service.update_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id, {'price': 6.00})
    retrieved_menu_item = menu_item_service.get_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id)

    assert math.isclose(updated_menu_item.price, retrieved_menu_item.price)
    assert not math.isclose(created_menu_item.price, retrieved_menu_item.price)
    assert math.isclose(retrieved_menu_item.price, 6.00)

def test_update_menu_item_name(test_data):
    (_, restaurant, menu) = test_data

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    updated_menu_item = menu_item_service.update_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id, {'name': 'New title'})
    retrieved_menu_item = menu_item_service.get_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id)

    assert created_menu_item.name != retrieved_menu_item.name
    assert updated_menu_item.name == retrieved_menu_item.name
    assert retrieved_menu_item.name == 'New title'

def test_update_menu_item_name_and_price_at_once(test_data):
    (_, restaurant, menu) = test_data

    menu_item_patch = {
        'name': 'New title',
        'price': 6.00,
    }

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    updated_menu_item = menu_item_service.update_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id, menu_item_patch)

    assert updated_menu_item.name == 'New title'
    assert math.isclose(updated_menu_item.price, 6.00)

def test_update_menu_item_with_empty_changeset_does_nothing(test_data):
    (_, restaurant, menu) = test_data

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    updated_menu_item = menu_item_service.update_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id, {})

    assert updated_menu_item.name == 'Test Item'
    assert math.isclose(updated_menu_item.price, 5.00)

def test_add_fake_attribute_to_menu_item_does_nothing(test_data):
    (_, restaurant, menu) = test_data

    created_menu_item = menu_item_service.create_menu_item(restaurant.id, menu.id, 'Test Item', 5.00)
    menu_item_service.update_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id, {'fake': 'parameter'})
    retrieved_menu_item = menu_item_service.get_menu_item_by_id(restaurant.id, menu.id, created_menu_item.id)

    with pytest.raises(AttributeError):
        retrieved_menu_item.fake
