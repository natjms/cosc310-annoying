import app.repositories.menu as repo
from app.schemas.menu import Menu

"""
Return a list of menus

Args:
	str - ID of the restaurant to query

return:
	list[Menu]
"""
def get_restaurant_menus(restaurant_id: str) -> list[Menu]:
	return repo.get_all_menus(restaurant_id)

