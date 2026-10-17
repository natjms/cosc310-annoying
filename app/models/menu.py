from pydantic import BaseModel
from ulid import ULID


class Menu(BaseModel):
    id: ULID
    restaurant_id: ULID
    name: str
