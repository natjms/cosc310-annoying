from pydantic import BaseModel


class MenuItem(BaseModel):
    id: str | None  # None is used for creating a new model that is yet to be saved to the database.
    name: str
    price: float
    is_active: bool
