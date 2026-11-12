from abc import update_abstractmethods

from ulid import ULID

from app.models.restaurant import Restaurant
from app.repositories.restaurant import restaurants
from app.repositories.user import users
from app.repositories.repo import UniqueError
from app.exceptions import MissingValueException


def list_all_restaurants() -> list[Restaurant]:
    return restaurants.select()


def find_restaurant_by_id(restaurant_id: ULID | str) -> Restaurant:
    try:
        return restaurants.unique(id=restaurant_id)
    except UniqueError:
        raise MissingValueException("The given restaurant does not exist")


def create_restaurant(owner_id: ULID | str, name: str) -> Restaurant:
    try:
        user = users.unique(id=owner_id)
    except UniqueError:
        raise MissingValueException("No user with the given ID exists")

    return restaurants.create(owner_id=owner_id, name=name)


def search_restaurants(query: str) -> list[Restaurant]:
    return restaurants.select(name=query)


def update_restaurant(restaurant_id: str, data: dict) -> Restaurant:
    if "owner_id" in data:
        try:
            user = users.unique(id=data["owner_id"])
        except UniqueError:
            raise MissingValueException("No user with the given ID exists")

    data = {k: v for k, v in data.items() if v is not None}
    return restaurants.update(id=restaurant_id, **data)


def delete_restaurant(restaurant_id: ULID) -> None:
    restaurants.delete(id=restaurant_id)
