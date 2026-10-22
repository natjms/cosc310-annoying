from abc import update_abstractmethods

from ulid import ULID

from app.models.restaurant import Restaurant
from app.repositories.restaurant import restaurants

def list_all_restaurants() -> list[Restaurant]:
    return restaurants.select()

def find_restaurant_by_id(restaurant_id: ULID | str) -> Restaurant:
    return restaurants.unique(id=restaurant_id)

def create_restaurant(owner_id: ULID | str, name: str) -> Restaurant:
    return restaurants.create(owner_id=owner_id, name=name)

def search_restaurants(query: str) -> list[Restaurant]:
    return restaurants.select(name=query)

def update_restaurant(restaurant_id: str, data: dict) -> Restaurant:
    data = {k: v for k, v in data.items() if v is not None}
    return restaurants.update(id=restaurant_id, **data)
