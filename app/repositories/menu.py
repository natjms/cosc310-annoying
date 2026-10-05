from app.exceptions import MissingValueException
from app.schemas.menu import Menu
from typing import TypeAlias
import os
import json

DATA_BASE_PATH = os.path.join(os.environ['DATA_DIR'], 'menus.json')

MenuCollection: TypeAlias = dict[str, dict[str, Menu]]

"""
Load the menu collection and return it

Returns:
	MenuCollection
"""
def _load_raw_menu_json() -> MenuCollection:
	with open(DATA_BASE_PATH, 'r') as f:
		return json.load(f)

"""
Return all menus associated with a restaurant. Raises a MissingValueException
if no restaurant exists with the given ID

Args:
	str	- restaurant_id

Returns:
	list[Menu]
"""
def get_all_menus(restaurant_id: str) -> list[Menu]:
	try:
		return list(_load_raw_menu_json()[restaurant_id].values())
	except KeyError:
		raise MissingValueException(f'No restaurant with id {restaurant_id} exists')
	
"""
Return a particular menu associated with a restaurant and all its items. Raises
a MissingValueException if no such menu exists, or if the restaurant doesn't exist

Args:
	str - ID of the restaurant
	menu_name - The name of the menu

Returns:
	Menu
"""
def get_menu(restaurant_id: str, menu_id: str) -> Menu:
	menus = _load_raw_menu_json()

	try:
		restaurant_menus = menus[restaurant_id]
	except KeyError:
		raise MissingValueException(f'Restaurant {restaurant_id} does not exist')

	try:
		menu = restaurant_menus[menu_id]
	except KeyError:
		raise MissingValueException(f'Menu {menu_id} is not a menu of restaurant {restaurant_id}')

	return menu

