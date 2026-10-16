from json import load, dump

from app.repositories import get_repository_data_file_path
from app.models.restaurant import Restaurant


FILENAME = "restaurants.json"


def create_restaurant(restaurant: Restaurant) -> Restaurant:
    JSON_INDENT = 4


    file_path = get_repository_data_file_path(FILENAME)
    
    with open(file_path) as file:
        data = load(file)

    restaurant_key, updated_data = _add_restaurant_to_data(data, restaurant)

    with open(file_path, "w") as file:
        dump(updated_data, file, indent=JSON_INDENT)

    return read_restaurant(restaurant_key)


def read_restaurant(id: str) -> Restaurant:  # TODO Finish this.
    restaurant = Restaurant(
        id=id,
        owner_id="",
        name="",
        description="",
        address={},
        phone_number="",
        is_active=True,
        cuisine_ids=set(),
        menus={},
    )

    return restaurant


def update_restaurant(restaurant: Restaurant) -> Restaurant:  # TODO Finish this.
    return restaurant


def delete_restaurant(id: str) -> Restaurant:  # TODO Finish this.
    restaurant = Restaurant(
        id=id,
        owner_id="",
        name="",
        description="",
        address={},
        phone_number="",
        is_active=True,
        cuisine_ids=set(),
        menus={},
    )

    return restaurant


def _add_restaurant_to_data(data: dict, restaurant: Restaurant) -> tuple[str, dict]:
    FIRST_KEY = "1"


    if restaurant.id:
        raise ValueError("A restaurant ID must be set automatically.")

    restaurant_key = FIRST_KEY if not data else _get_next_key(data)
    
    data[restaurant_key] = restaurant.model_dump()
    
    return restaurant_key, data


def _get_next_key(data_json: dict) -> str:
    keys = data_json.keys()

    largest_key = max(keys, key=int)
    largest_key_int = int(largest_key)

    restaurant_key_int = largest_key_int + 1
    return str(restaurant_key_int)
