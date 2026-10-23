import pytest
from pydantic import ValidationError
from ulid import ULID
from app.models.menu import Menu
from app.models.menu_item import MenuItem

def test_menu_valid_with_items():
    menu_id=ULID()
    restaurant_id=ULID()
    item_id=ULID()

    item=MenuItem(id=item_id,name="Burger",price=5.0,is_active=True)
    menu = Menu(
        id=menu_id,
        restaurant_id=restaurant_id,
        name="Lunch Menu",
        items={item.id: item}
        )

    assert menu.id == menu_id
    assert menu.is_active is True
    assert menu.items[item_id].name == "Burger"

def test_menu_defaults():
    menu = Menu(id=ULID(),name="empty menu",restaurant_id=None)
    assert menu.restaurant_id is None
    assert menu.items == {}
    assert menu.is_active is True

def test_menu_invalid_items_nested():
    with pytest.raises(ValidationError):
        Menu(id=ULID(),name="Incorrect Menu",items={ULID():"invalid item"})
