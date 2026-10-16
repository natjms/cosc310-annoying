from ulid import ULID

from app.models.restaurant import Restaurant
from app.repositories.restaurant import restaurants

def list_all_restaurants() -> list[Restaurant]:
    return restaurants.select()

def find_restaurant_by_id(restaurant_id: ULID | str) -> Restaurant:
    return restaurants.unique(id=restaurant_id)

def create_restaurant(owner_id: ULID | str, name: str) -> Restaurant:
    return restaurants.create(owner_id=owner_id, name=name)
