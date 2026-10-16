from app.models.restaurant import Restaurant
from app.repositories.restaurant import create_restaurant, read_restaurant

# Typical

def test_valid_restaurant():
    restaurant = Restaurant(
        id=None,
        owner_id="",
        name="",
        description="",
        address={},
        phone_number="",
        is_active=True,
        cuisine_ids=set(),
        menus={},
    )

    create_restaurant(restaurant)

    expected_restaurant = read_restaurant()


# Extreme

def test_empty_file():
    pass


# Erroneous

def test_non_existent_file():
    pass
