from pydantic import BaseModel
from ulid import ULID

from . import MenuItem


class Menu(BaseModel):
    id: ULID
    restaurant_id: ULID | None
    name: str
    is_active: bool = True
    items: dict[ULID, MenuItem] = {}


class PostMenuRequest(BaseModel):
    name: str
