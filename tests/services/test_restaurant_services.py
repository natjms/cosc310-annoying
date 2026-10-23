from ulid import ULID
import pytest

from app.services import restaurant as restaurant_service
from app.services import user as user_service
from app.repositories.restaurant import restaurants as restaurant_repo
from app.repositories.user import users as user_repo
from app.exceptions import MissingValueException

@pytest.fixture
def test_data():
    user = user_service.create_user()
    restaurant = restaurant_service.create_restaurant(user.id, 'Test Restaurant')

    yield (user, restaurant)

    restaurant_repo.delete(id=restaurant.id)
    user_repo.delete(id=user.id)

def test_create_and_get_single_restaurant(test_data):
    (user, _) = test_data

    new_restaurant = restaurant_service.create_restaurant(user.id, 'New Restaurant')
    retrieved_restaurant = restaurant_service.find_restaurant_by_id(new_restaurant.id)

    assert new_restaurant.id == retrieved_restaurant.id

    restaurant_repo.delete(id=new_restaurant.id)

def test_create_restaurant_with_invalid_owner_fails():
    with pytest.raises(MissingValueException):
        restaurant_service.create_restaurant(ULID(), 'New Restaurant')

def test_retrieve_single_restaurant(test_data):
    (_, restaurant) = test_data
    assert restaurant_service.find_restaurant_by_id(restaurant.id) == restaurant

def test_retrieve_nonexistent_restaurant_raises(test_data):
    (_, restaurant) = test_data
    with pytest.raises(MissingValueException):
        restaurant_service.find_restaurant_by_id(ULID())

def test_list_all_restaurants_with_create(test_data):
    (user, _) = test_data
    # There's only been one created initially in the test_data fixture
    all_restaurants = restaurant_service.list_all_restaurants()
    assert len(all_restaurants) == 1

    new_restaurant = restaurant_service.create_restaurant(user.id, 'New Restaurant')
    all_restaurants = restaurant_service.list_all_restaurants()
    assert len(all_restaurants) == 2

    restaurant_repo.delete(id=new_restaurant.id)

def test_search_restaurants(test_data):
    (user, _) = test_data
    new_restaurant = restaurant_service.create_restaurant(user.id, '777')
    search_results = restaurant_service.search_restaurants('777')
    assert len(search_results) == 1

    restaurant_repo.delete(id=new_restaurant.id)

def test_search_restaurants_with_non_matching_query(test_data):
    (user, _) = test_data
    search_results = restaurant_service.search_restaurants('777')
    assert len(search_results) == 0

def test_update_restaurant_name(test_data):
    (_, restaurant) = test_data
    updated_restaurant = restaurant_service.update_restaurant(restaurant.id, {'name': 'Updated Name'})
    retrieved_restaurant = restaurant_service.find_restaurant_by_id(restaurant.id)
    assert updated_restaurant.name == retrieved_restaurant.name

def test_update_restaurant_owner(test_data):
    (_, restaurant) = test_data
    new_user = user_service.create_user()
    updated_restaurant = restaurant_service.update_restaurant(restaurant.id, {'owner_id': new_user.id})
    retrieved_restaurant = restaurant_service.find_restaurant_by_id(restaurant.id)
    assert updated_restaurant.owner_id == retrieved_restaurant.owner_id

    user_repo.delete(id=new_user.id)

def test_update_restaurant_owner_to_nonexistent_owner(test_data):
    (_, restaurant) = test_data
    with pytest.raises(MissingValueException):
        updated_restaurant = restaurant_service.update_restaurant(restaurant.id, {'owner_id': ULID()})
