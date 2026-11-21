from pydantic import BaseModel
from ulid import ULID

from app.models import MenuItem


class Menu(BaseModel):
    id: ULID
    restaurant_id: ULID
    name: str
    is_active: bool = True
    items: dict[ULID, MenuItem] = {}


class PostMenuRequest(BaseModel):
    restaurant_id: ULID
    name: str


class PatchMenuRequest(BaseModel):
    name: str | None = None
    is_active: bool | None = None
