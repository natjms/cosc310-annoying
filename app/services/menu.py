from ulid import ULID

from app.models.menu import Menu
from app.repositories.menu import menus

def list_restaurant_menus(restaurant_id: ULID | str) -> list[Menu]:
    return menus.select(restaurant_id=restaurant_id)

def create_menu(restaurant_id: ULID | str, name: str) -> Menu:
    return menus.create(restaurant_id=restaurant_id, name=name)

def delete_menu(_restaurant_id: ULID | str, menu_id: ULID | str) -> None:
	menus.delete(id=menu_id)
