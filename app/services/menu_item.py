from app.models.menu_item import MenuItem
from app.models.menu import Menu
from app.repositories.menu import menus
from app.exceptions import MissingValueException

from app.services import assume_empty_string_is_undeclared, select_only_model_attributes

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

def update_menu_item_by_id(
	restaurant_id: str,
	menu_id: str,
	menu_item_id: str,
	menu_item_overwrite: dict
) -> MenuItem:
	update_data = select_only_model_attributes(menu_item_overwrite)
	update_data = assume_empty_string_is_undeclared(update_data)

	try:
		menu = menus.unique(id=menu_id, restaurant_id=restaurant_id)
		updated_menu_items = menu.items
		updated_menu_items[menu_item_id] = {**updated_menu_items, **update_data}
		menus.update(id=menu_id, items=updated_menu_items)
	except Exception:
		raise MissingValueException(f"Menu or Item could not be found")
