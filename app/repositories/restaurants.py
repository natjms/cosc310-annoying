import json

from app.schemas.restaurant import Restaurant

from . import get_repo_data_path

RESTAURANTS_PATH = get_repo_data_path("restaurants")

"""
Loads the restaurants from the data file and validates them.
Returns:
    list[Restaurant]: The list of restaurants.
"""
def load_restaurants() -> list[Restaurant]:
    with open(RESTAURANTS_PATH) as file:
        restaurants_array = json.load(file)

    if type(restaurants_array) != list:
        raise ValueError("restaurants.json must contain a list")

    return [Restaurant.model_validate(restaurant) for restaurant in restaurants_array]
