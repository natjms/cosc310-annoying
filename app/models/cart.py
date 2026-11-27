from datetime import datetime

from pydantic import BaseModel
from ulid import ULID

from .cart_item import CartItem


class Cart(BaseModel):
    updated_at: datetime
    user_id: ULID
    id: ULID
    restaurant_id: ULID
    is_active: bool = True
    items: dict[ULID, CartItem] = {}
