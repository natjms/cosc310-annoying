from pydantic import BaseModel
from ulid import ULID

# Note: unlike many of our models, this one is not actually represented by its
# own repository. Rather, it's entirely dependent on the Menu repo; each menu
# has a dict mapping ULID: MenuItem
class MenuItem(BaseModel):
    id: ULID
    name: str
    price: float
    is_active: bool
