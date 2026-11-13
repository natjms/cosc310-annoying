from app.schemas.menu import Menu


class MenuService:
    def __init__(self, repository: Repo = Repo()) -> None:
        self._repository = repository

    def get_all_menus_by_restaurant_id(self, id: str) -> list[Menu]:
        return self._repository.select(restaurant_id=id)

    def create_menu(
            self,
            *,
            restaurant_id: str,
            name: str,
            is_active: bool,
        ) -> Menu:
        raise NotImplementedError()

    def update_menu(
            self,
            *,
            id: str,
            restaurant_id: str | None = None,
            name: str | None = None,
            is_active: bool | None = None,
        ) -> Menu:
        raise NotImplementedError()
