from pydantic import BaseModel


class Menu(BaseModel):
    id: str | None  # None is used for creating a new model that is yet to be saved to the database.
    name: str
    is_active: bool
    items: dict
