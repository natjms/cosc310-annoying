from ulid import ULID

from app.models.menu_item import MenuItem
from app.models.menu import Menu
from app.repositories.menu import menus
from app.repositories.repo import UniqueError
from .utils import maybe_ulid
from app.exceptions import MissingValueException

def get_all_menu_items(menu_id: str) -> list[MenuItem]:
    try:
        menu = menus.unique(id=menu_id)
        return [item for item in menu.items.values()]
    except UniqueError:
        raise MissingValueException(f"The requested menu does not exist")

def get_menu_item_by_id(
    menu_id: str,
    menu_item_id: str | ULID
) -> MenuItem:
    try:
        menu = menus.unique(id=menu_id)
        menu_item = menu.items[maybe_ulid(menu_item_id)]
        return menu_item
    except UniqueError:
        raise MissingValueException("The requested menu does not exist")
    except KeyError:
        raise MissingValueException("Menu item cannot be found")

def update_menu_item_by_id(
    menu_id: str,
    menu_item_id: str,
    menu_item_overwrite: dict
) -> MenuItem:
    menu_item_overwrite = {k: v for k, v in menu_item_overwrite.items() if v is not None}
    try:
        menu = menus.unique(id=menu_id)
        updated_menu_items = menu.items

        updated_item = {**menu.items[maybe_ulid(menu_item_id)].model_dump(), **menu_item_overwrite}
        updated_menu_items[maybe_ulid(menu_item_id)] = MenuItem(**updated_item)

        menus.update(id=menu_id, items=updated_menu_items)
        return menus.unique(id=menu_id).items[maybe_ulid(menu_item_id)]
    except KeyError:
        raise MissingValueException("Menu item cannot be found")
    except UniqueError:
        raise MissingValueException("The requested menu does not exist")

def create_menu_item(
    menu_id: str,
    name: str,
    price: float
) -> MenuItem:
    try:
        menu = menus.unique(id=menu_id)
        updated_menu_items = menu.items
        new_id = ULID()

        updated_menu_items[new_id] = MenuItem(name=name, price=price, id=new_id, is_active=True)
        menus.update(id=menu_id, items=updated_menu_items)
        return menus.unique(id=menu_id).items[new_id]
    except UniqueError:
        raise MissingValueException(f"The requested menu does not exist")
