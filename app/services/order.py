from datetime import datetime

from ulid import ULID

from app.exceptions import MissingValueException
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.cart import Cart
from app.repositories.order import orders
from app.repositories.repo import UniqueError
from app.services.cart import clear_cart, get_or_create_cart
from app.services.menu_item import get_menu_item_by_id

from .utils import maybe_ulid


def create_order_from_cart(user_id: ULID, restaurant_id: ULID) -> Order:
    # get or create cart
    cart = get_or_create_cart(user_id, restaurant_id)
    # empty cart check since empty carts can't be used to place an order
    if not cart.items:
        raise MissingValueException("can not place an order since this cart is empty!")

    # get the price using menu-item and copy items
    order_items = {}
    total = 0.0

    for menu_item_id, cart_item in cart.items.items():
        menu_item = get_menu_item_by_id(str(cart_item.menu_id), cart_item.menu_item_id)
        order_item = OrderItem(
            id=ULID(),
            menu_item_id=cart_item.menu_item_id,
            quantity=cart_item.quantity,
            price_at_order_time=menu_item.price,
        )
        order_items[order_item.id] = order_item
        total += menu_item.price * cart_item.quantity

    # create order
    order = orders.create(
        user_id=user_id,
        restaurant_id=restaurant_id,
        updated_at=datetime.now(),
        items=order_items,
        price=total,
        status="pending",
    )
    # clearing cart because epic says so
    clear_cart(user_id, restaurant_id)
    return order


def get_all_orders(user_id: ULID) -> list[Order]:
    return orders.select(user_id=user_id)


def get_order_by_id(user_id: ULID, order_id: ULID) -> Order:
    try:
        return orders.unique(id=order_id, user_id=user_id)
    except UniqueError:
        raise MissingValueException("order not found")


def cancel_order(user_id: ULID, order_id: ULID) -> Order:
    get_order_by_id(user_id, order_id)
    return orders.update(id=order_id, status="cancelled")


def update_order(user_id: ULID, order_id: ULID, **kwargs) -> Order:
    get_order_by_id(user_id, order_id)
    return orders.update(id=order_id, **kwargs)
