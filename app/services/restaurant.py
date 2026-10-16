import app.repositories.restaurant as repo
from app.schemas.restaurant import Restaurant

def get_all_restaurants() -> list[Restaurant]:
    return repo.load_restaurants()

def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    return repo.read_restaurant(restaurant_id)
