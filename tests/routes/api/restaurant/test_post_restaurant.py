import pytest

from app.models import Restaurant
from app.routes.api.restaurant import get_service, post_restaurant
from app.schemas import PostRestaurantRequest
from app.main import app


class RestaurantServiceStub:
    def __init__(self, restaurant: Restaurant) -> None:
        self._restaurant = restaurant

    def create_restaurant(
        self,
        *,
        user_id: str,
        name: str,
        description: str,
        address: str,
        phone_number: str,
        is_active: bool,
    ) -> Restaurant:
        return self._restaurant


@pytest.mark.parametrize(
        
)
def test_valid_request():
    request = PostRestaurantRequest(
        name="",
        description="",
        address="",
        phone_number="",
        is_active=True,
    )

    expected_restaurant = Restaurant(
        id=,
        owner_id: str,
        name: str,
        description: str,
        address: str,
        phone_number: str,
        is_active: bool
    )

    restaurant = post_restaurant(request, FakeRestaurantService())



