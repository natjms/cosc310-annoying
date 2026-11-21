from datetime import datetime

from pydantic import BaseModel
from ulid import ULID

from .order_item import OrderItem


class Order(BaseModel):
    updated_at: datetime
    user_id: ULID
    id: ULID
    restaurant_id: ULID | None
    is_active: bool = True
    items: dict[ULID, OrderItem] = {}
    status: str = "pending"
    total_price: float = 0
