from app.models.menu import Menu
from app.repositories.repo import Repo

menus = Repo('menus', Menu, indexed_fields=['restaurant_id'])
