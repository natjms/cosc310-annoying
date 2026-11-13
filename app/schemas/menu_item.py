from pydantic import BaseModel
from ulid import ULID

from app.models import MenuItem


class BaseMenuItemRequest(BaseModel):
    name: str
    price: float
    is_active: bool


class PatchMenuItemRequest(BaseModel):
    name: str | None = None
    price: float | None = None
    is_active: bool | None = None


class PostMenuItemRequest(BaseMenuItemRequest):
    pass

    
class MenuItemResponse(BaseMenuItemRequest):
    id: ULID

    def __init__(self, menu_item: MenuItem):
            pass  # Create from restaurant instance.