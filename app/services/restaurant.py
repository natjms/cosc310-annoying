from app.schemas.restaurant import Restaurant
from app.repositories.repo import Repo, UniqueError
from app.exceptions import MissingValueException


class RestaurantService():
    def __init__(
            self,
            restaurant_repository: Repo = Repo(),
            user_repository: Repo = Repo(),
        ) -> None:
        self._restaurant_repository = restaurant_repository
        self._user_repository = user_repository

    def get_all_restaurants(self) -> list[Restaurant]:
        return self._restaurant_repository.select()

    def search_restaurants(self, query: str) -> list[Restaurant]:
        return self._restaurant_repository.select(name=query)

    def get_restaurant_by_id(self, id: str) -> Restaurant:
        try:
            return self._restaurant_repository.unique(id=id)
        except UniqueError:
            raise MissingValueException('The given restaurant does not exist')

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

        """
        restaurant = restaurant_repository.get_by_id(id)

        user_owns_restaurant = restaurant.is_owned_by(user_id)
        if not user_owns_restaurant:
            raise ForbiddenError("You must own the restaurant you are trying to edit.")

        update the restaurant...
        """

    def delete_restaurant_by_id(
            self,
            *,
            id: str,
            user_id: str,
        ) -> Restaurant:
        raise NotImplementedError()
