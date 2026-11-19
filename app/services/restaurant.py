from app.models import Restaurant
from app.repositories.repo import Repo


class RestaurantService():
    def __init__(
            self,
            restaurant_repository: Repo = Repo(),
            user_repository: Repo = Repo(),
        ) -> None:
        self._restaurant_repository = restaurant_repository
        self._user_repository = user_repository

    def get_all_restaurants(self) -> list[Restaurant]:
        raise NotImplementedError()

    def search_restaurants(self, query: str) -> list[Restaurant]:
        raise NotImplementedError()

    def get_restaurant_by_id(self, id: str) -> Restaurant:
        raise NotImplementedError()

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
        raise NotImplementedError()

    def update_restaurant(
            self,
            *,
            id: str,
            user_id: str,
            name: str | None = None,
            description: str | None = None,
            address: str | None = None,
            phone_number: str | None = None,
            is_active: bool | None = None,
        ) -> Restaurant:
        raise NotImplementedError()

    def delete_restaurant_by_id(
            self,
            id: str,
            user_id: str,
        ) -> Restaurant:
        raise NotImplementedError()
