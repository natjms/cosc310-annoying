from typing import Annotated

from pydantic import AfterValidator, BaseModel
from ulid import ULID

from app import validators as v


# Note: unlike many of our models, this one is not actually represented by its
# own repository. Rather, it's entirely dependent on the Menu repo; each menu
# has a dict mapping ULID: MenuItem
class MenuItem(BaseModel):
    id: ULID
    name: str
    price: float
    is_active: bool


class PostMenuItemRequest(BaseModel):
    name: Annotated[str | None, AfterValidator(v.nonempty_string)]
    price: Annotated[float | None, AfterValidator(v.positive_float)]


class PatchMenuItemRequest(BaseModel):
    name: Annotated[str | None, AfterValidator(v.coerce_empty_string_to_none)] = None
    price: Annotated[float | None, AfterValidator(v.positive_float)] = None
