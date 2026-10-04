import pytest

import app.repositories.menu as repo
import app.schemas.menu as schema

def test_load_menu():
	menu = repo._load_raw_menu_json()
	for key, value in menu.items():
		assert isinstance(key, str)
		assert isinstance(value, list)

def test_get_all_menus():
	menus = repo.get_all_menus('1')
	assert menus[0]['name'] == 'Test Menu'

def test_get_all_menus_incorrect_restaurant():
	with pytest.raises(KeyError) as e:
		repo.get_all_menus('This is not an extant ID')

def test_get_specific_menu():
	menu = repo.get_menu('1', 'Test Menu')
	assert menu['items'][0]['name'] == 'Fiddlehead Soup'

def test_get_specific_menu_incorrect_restaurant():
	with pytest.raises(KeyError) as e:
		repo.get_menu('Invalid restaurant ID', 'Test Menu')

def test_get_specific_nonexistant_menu():
	with pytest.raises(KeyError) as e:
		repo.get_menu('1', 'Nonexistant Menu')
