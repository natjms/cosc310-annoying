import app.services.menu as service
import pytest

from app.exceptions import MissingValueException

def test_get_all_menus():
	menus = service.get_restaurant_menus('1')
	assert menus[0]['name'] == 'Test Menu'

def test_get_all_menus_for_nonexistant_restaurant():
	with pytest.raises(MissingValueException):
		service.get_restaurant_menus('Nonexistant restaurant ID')
