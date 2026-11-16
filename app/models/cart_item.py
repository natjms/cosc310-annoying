from typing import Annotated

from pydantic import AfterValidator, BaseModel
from ulid import ULID

from app import validators as v


# Note: unlike many of our models, this one is not actually represented by its
# own repository. Rather, it's entirely dependent on the Cart repo; each cart
# has a dict mapping ULID: CartItem
class CartItem(BaseModel):
    id: ULID
    menu_item_id: ULID
    quantity: int


class PostCartItemRequest(BaseModel):
    menu_item_id: Annotated[str | None, AfterValidator(v.nonempty_string)]
    quantity: Annotated[float | None, AfterValidator(v.positive_int)]


class PatchCartItemRequest(BaseModel):
    quantity: Annotated[float | None, AfterValidator(v.positive_int)] = None
