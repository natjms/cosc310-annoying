from pydantic import BaseModel
from ulid import ULID


class Menu(BaseModel):
    id: ULID
    restaurant_id: ULID | None
    name: str
    is_active: bool = True
    items: dict = {}
