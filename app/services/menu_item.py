from app.models.menu_item import MenuItem


def get_all_menu_items(restaurant_id: str, menu_id: str) -> MenuItem:
    raise NotImplementedError()


def get_menu_item_by_id(
    restaurant_id: str,
    menu_id: str,
    menu_item_id: str
) -> MenuItem:
    raise NotImplementedError()
