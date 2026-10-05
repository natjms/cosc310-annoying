import pytest

import app.repositories.menu as repo
import app.schemas.menu as schema

from app.exceptions import MissingValueException

# This effectively tests that we can load the test data menus.json file
def test_load_menu():
	menus = repo._load_raw_menu_json()
	assert menus is not None

def test_get_all_menus():
	menus = repo.get_all_menus('1')
	assert menus[0]['name'] == 'Test Menu'

def test_get_all_menus_incorrect_restaurant():
	with pytest.raises(MissingValueException):
		repo.get_all_menus('This is not an extant ID')

def test_get_specific_menu():
	menu = repo.get_menu('1', '1')
	assert menu['name'] == 'Test Menu'

def test_get_specific_menu_incorrect_restaurant():
	with pytest.raises(MissingValueException):
		repo.get_menu('Invalid restaurant ID', '1')

def test_get_specific_nonexistant_menu():
	with pytest.raises(MissingValueException):
		repo.get_menu('1', 'Nonexistant Menu')
