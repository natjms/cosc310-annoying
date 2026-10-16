from pydantic import BaseModel


class Restaurant(BaseModel):
    id: str | None  # None is used for creating a new model that is yet to be saved to the database.
    owner_id: str
    name: str
    description: str
    address: dict
    phone_number: str
    is_active: bool
    cuisine_ids: set[int]
    menus: dict
