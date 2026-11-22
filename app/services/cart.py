from datetime import datetime

from ulid import ULID

from app.exceptions import MissingValueException
from app.models.cart import Cart
from app.models.cart_item import (  # nts: eval if this is necessary
    CartItem,
    PostCartItemRequest,
)
from app.repositories.cart import carts
from app.repositories.menu import menus
from app.repositories.repo import UniqueError

from .utils import maybe_ulid


def get_or_create_cart(user_id: ULID, restaurant_id: ULID) -> Cart:
    try:
        return carts.unique(user_id=user_id, restaurant_id=restaurant_id)
    except UniqueError:
        return carts.create(
            user_id=user_id, restaurant_id=restaurant_id, updated_at=datetime.now()
        )


def get_active_cart(user_id: ULID) -> Cart:
    active_carts = carts.select(
        user_id=user_id,
        is_active=True,
        _order_by="updated_at",
        _order_desc=True,
        _limit=1,
    )
    if not active_carts:
        raise MissingValueException("no active cart was found")
    return active_carts[0]


def activate_cart(user_id: ULID, restaurant_id: ULID) -> Cart:
    user_carts = carts.select(user_id=user_id)
    for c in user_carts:
        if c.is_active:
            carts.update(id=c.id, is_active=False)
    target_cart = get_or_create_cart(user_id, restaurant_id)
    return carts.update(id=target_cart.id, is_active=True)


def add_item_to_cart(
    user_id: ULID, restaurant_id: ULID, menu_item_id: ULID, quantity: int
) -> Cart:
    cart = get_or_create_cart(user_id, restaurant_id)
    if menu_item_id in cart.items:
        cart.items[menu_item_id].quantity += quantity
    else:
        new_id = ULID()
        cart.items[menu_item_id] = CartItem(
            id=new_id, menu_item_id=menu_item_id, quantity=quantity
        )
    return carts.update(id=cart.id, items=cart.items, updated_at=datetime.now())


def update_cart_item(
    user_id: ULID, restaurant_id: ULID, menu_item_id: ULID, quantity: int
) -> Cart:
    cart = get_or_create_cart(user_id, restaurant_id)
    if menu_item_id not in cart.items:
        raise MissingValueException(
            "item not in cart"
        )
    if quantity <= 0:
        if menu_item_id in cart.items:
            del cart.items[menu_item_id]
    else:
        if menu_item_id in cart.items:
            cart.items[menu_item_id].quantity = quantity
        else:
            cart.items[menu_item_id] = CartItem(
                id=ULID(), menu_item_id=menu_item_id, quantity=quantity
            )
    return carts.update(id=cart.id, items=cart.items, updated_at=datetime.now())


def clear_cart(user_id: ULID, restaurant_id: ULID) -> Cart:
    cart = get_or_create_cart(user_id=user_id, restaurant_id=restaurant_id)
    return carts.update(id=cart.id, items={}, updated_at=datetime.now())
