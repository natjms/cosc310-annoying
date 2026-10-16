import app.repositories.restaurant as repo
from app.models.restaurant import Restaurant

def get_all_restaurants() -> list[Restaurant]:
    raise NotImplementedError()

def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    raise NotImplementedError()
