from pydantic import BaseModel
from ulid import ULID
from datetime import datetime
from .cart_item import CartItem


class Cart(BaseModel):
    updated_at: datetime
    user_id: ULID
    id: ULID
    restaurant_id: ULID | None
    is_active: bool = True
    items: dict[ULID, CartItem] = {}
