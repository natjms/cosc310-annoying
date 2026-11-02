from pydantic import BaseModel
from ulid import ULID


class MenuBase(BaseModel):
    name: str
    is_active: bool


class PatchMenuRequest(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class PostMenuRequest(MenuBase):
    restaurant_id: ULID  # This could be passed in the URL if we change the url design: POST api/restaurant/{restaurant_id}/menu. At the time of writing this comment, our design is this instead: POST /api/menu.

    
class MenuResponse(MenuBase):
    id: ULID
    restaurant_id: ULID
