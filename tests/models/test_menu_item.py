import pytest
from pydantic import ValidationError
from ulid import ULID
from app.models.menu_item import MenuItem

def test_menu_item_valid():
    item_id = ULID()
    item = MenuItem(id=item_id, name="Burger", price=10.50,is_active=True)
    assert item.id == item_id
    assert item.name == "Burger"
    assert item.price == 10.50
    assert item.is_active is True

def test_menu_item_type_coercion():
    item = MenuItem(id=ULID(),name="Burger",price="5.99",is_active=False)
    assert item.price == 5.99

def test_menu_item_missing_required_fields():
    with pytest.raises(ValidationError):
        MenuItem(id=ULID())