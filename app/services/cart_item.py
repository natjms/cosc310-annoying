""" from ulid import ULID

from app.models.menu_item import MenuItem
from app.models.menu import Menu
from app.repositories.menu import menus
from app.repositories.repo import UniqueError
from .utils import maybe_ulid
from app.exceptions import MissingValueException


def get_cart_item_by_id():

def create_cart_item():


def update_cart_item_by_id(id: ULID, user_id: ULID, restaurant_id: ULID, cart_id: ULID, cart_item_id: ULID, cart_item_overwrite: dict) -> CartItem:
    cart_item_overwrite = {k:v for k, v in cart_item_overwrite.items() if v is not None}
    try:
        cart = carts.unique(id=,restaurant_id=)
        updated_cart_items = cart.items

        updated_item = {**cart.items[maybe_ulid(cart_item_id)].model_dump(), **cart_item_overwrite}
        updated_cart_items[maybe_ulid(cart_item_id)] = CartItem(**updated_item)
        carts.update(id=,items=)
        return cart.unique(id,restaurantid)
    except UniqueError:
        raise MissingValueException("either the user or the cart or the restaurant can't be found")
    except KeyError:
        raise MissingValueException("cart item can't be found")
 """
