from typing import Annotated

from pydantic import AfterValidator, BaseModel
from ulid import ULID

from app import validators as v


# Note: unlike many of our models, this one is not actually represented by its
# own repository. Rather, it's entirely dependent on the Order repo; each order
# has a dict mapping ULID: OrderItem
class OrderItem(BaseModel):
    id: ULID
    menu_id: ULID
    menu_item_id: ULID
    quantity: int
    price_at_order_time: float
