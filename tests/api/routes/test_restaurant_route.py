from fastapi.testclient import TestClient
import pytest
from app import app
from ulid import ULID

from app.services import restaurant as restaurant_service
from app.services import user as user_service
from app.repositories.restaurant import restaurants as restaurant_repo
from app.repositories.user import users as user_repo
from app.exceptions import MissingValueException

client = TestClient(app)

@pytest.fixture
def test_data():
    user = user_service.create_user()
    restaurant = restaurant_service.create_restaurant(user.id, 'Test Restaurant')

    yield (user, restaurant)

    restaurant_repo.delete(id=restaurant.id)
    user_repo.delete(id=user.id)

def test_cannot_get_nonexistant_restaurant():
    response = client.get(f'/api/restaurant/{ULID()}')
    assert response.status_code == 404

def test_create_and_retrieve_restaurant(test_data):
    (user, _) = test_data

    create_response = client.post('/api/restaurant/',
        headers={'Content-Type': 'application/json'},
        json={
            'owner_id': str(user.id),
            'name': 'Created Restaurant',
        }
    )

    new_restaurant_id = create_response.json()['id']
    assert create_response.status_code == 201

    retrieve_response = client.get(f'/api/restaurant/{new_restaurant_id}')
    assert retrieve_response.json()['name'] == 'Created Restaurant'

    restaurant_repo.delete(id=ULID.from_str(new_restaurant_id))

def test_attempt_to_create_restaurant_with_fake_user(test_data):
    create_response = client.post('/api/restaurant/',
        headers={'Content-Type': 'application/json'},
        json={
            'owner_id': str(ULID()),
            'name': 'Created Restaurant',
        }
    )

    assert create_response.status_code == 404

def test_update_restaurant(test_data):
    (_, restaurant) = test_data
    update_response = client.patch(f'/api/restaurant/{restaurant.id}',
        headers={'Content-Type': 'application/json'},
        json={ 'name': 'Updated Restaurant' }
    )

    assert update_response.status_code == 200

    retrieve_response = client.get(f'/api/restaurant/{restaurant.id}')
    assert retrieve_response.json()['name'] == 'Updated Restaurant'
