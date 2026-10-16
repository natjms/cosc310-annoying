import json

from app.repositories import get_repository_data_file_path
from app.schemas.restaurant import Restaurant


FILENAME = "restaurants.json"


def create_restaurant(restaurant: Restaurant) -> Restaurant:
    if restaurant.id:
        raise ValueError("A restaurant ID must be set automatically.")

    


def read_restaurant() -> Restaurant:
    return


def update_restaurant() -> Restaurant:
    return


def delete_restaurant() -> Restaurant:
    return
