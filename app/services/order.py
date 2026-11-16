from datetime import datetime

from ulid import ULID

from app.exceptions import MissingValueException
from app.models.order import Order
from app.models.order_item import OrderItem  # nts: eval if this is necessary
from app.repositories.repo import UniqueError

from .utils import maybe_ulid


def create_order_from_cart():
    pass


def get_all_orders():
    pass


def get_order_by_id():
    pass


def cancel_order():
    pass
