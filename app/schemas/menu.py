from pydantic import BaseModel

from app.models import Menu


class PostMenuRequest(BaseModel):
    restaurant_id: str
    name: str
    is_active: bool


class PatchMenuRequest(BaseModel):
    restaurant_id: str | None = None
    name: str | None = None
    is_active: bool | None = None


class DeleteMenuRequest(BaseModel):
    # Apparently, passing a request body for DELETE is bad HTTP practice. In future, we should move authentication to a JWT in the header or something similar.

    restaurant_id: str

    
class MenuResponse(BaseModel):
    id: str
    restaurant_id: str
    name: str
    is_active: bool

    def __init__(self, menu: Menu):
        raise NotImplementedError()
