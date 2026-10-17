from app.models.menu_item import MenuItem
from app.models.menu import Menu
from app.repositories.menu import menus
from app.exceptions import MissingValueException

def get_all_menu_items(restaurant_id: str, menu_id: str) -> list[MenuItem]:
    try:
        menu = menus.unique(id=menu_id, restaurant_id=restaurant_id)
    except Exception:
        raise MissingValueException(f"Menu {menu_id} not found for restaurant {restaurant_id}")
        return [MenuItem(**item_data) for item_data in menu.items.values()] # returns the dict type menu.items properly

def get_menu_item_by_id(
    restaurant_id: str,
    menu_id: str,
    menu_item_id: str
) -> MenuItem:
    try:
        menu = menus.unique(id=menu_id, restaurant_id=restaurant_id)
        item_data = menu.items[menu_item_id]
        return MenuItem(**item_data)
    except Exception:
        raise MissingValueException(f"Menu or Item could not be found")
