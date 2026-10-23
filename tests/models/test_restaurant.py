import pytest
from pydantic import ValidationError
from ulid import ULID
from app.models.restaurant import Restaurant,Address

def test_restaurant_valid():
    rest_id = ULID()
    owner_id = ULID()
    rest = Restaurant(id=rest_id,owner_id=owner_id,name="McDonalds")

    assert rest.id == rest_id
    assert rest.owner_id == owner_id
    assert rest.name == "McDonalds"
    assert isinstance(rest.address,Address)

def test_restaurant_defaults():
    rest = Restaurant(id=ULID(),owner_id=ULID(),name="Void")
    assert rest.description == ""
    assert rest.phone_number == ""
    assert rest.is_active is True
    assert rest.cuisine_ids == set()
    assert rest.address.city == ""

def test_restaurant_missing_name():
    with pytest.raises(ValidationError):
        Restaurant(id=ULID(),owner_id=ULID())
