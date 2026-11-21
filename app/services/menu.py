from ulid import ULID

from app.models.menu import Menu
from app.repositories.menu import menus


def list_restaurant_menus(restaurant_id: ULID | str) -> list[Menu]:
    return menus.select(restaurant_id=restaurant_id)


def create_menu(restaurant_id: ULID, name: str) -> Menu:
    return menus.create(restaurant_id=restaurant_id, name=name)


def delete_menu(menu_id: ULID | str) -> None:
    menus.delete(id=menu_id)


def get_menu_by_id(menu_id: ULID | str) -> Menu:
    return menus.unique(id=menu_id)


def update_menu(menu_id: ULID | str, updates: dict) -> Menu:
    return menus.update(id=menu_id, **updates)
