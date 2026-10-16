from json import load, dump

from app.repositories import get_repository_data_file_path
from app.models.restaurant import Restaurant


FILENAME = "restaurants.json"


def create_restaurant(restaurant: Restaurant) -> Restaurant:
    JSON_INDENT = 4


    if restaurant.id:
        raise ValueError("A restaurant ID must be set automatically.")

    file_path = get_repository_data_file_path(FILENAME)
    with open(file_path) as file:
        data_json = load(file)

    if data_json:
        keys = data_json.keys()
        largest_key = max(keys, key=int)
        largest_key_int = int(largest_key)
        restaurant_key_int = largest_key_int + 1
        restaurant_key = str(restaurant_key_int)
    else:
        restaurant_key = "1"

    restaurant_json = restaurant.model_dump_json()

    data_json[restaurant_key] = restaurant_json

    with open(file_path, "w") as file:
        dump(data_json, file, indent=JSON_INDENT)

    return read_restaurant(restaurant_key)


def read_restaurant(id: str) -> Restaurant:
    return


def update_restaurant() -> Restaurant:
    return


def delete_restaurant() -> Restaurant:
    return
