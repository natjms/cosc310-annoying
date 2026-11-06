from pydantic import BaseModel
from ulid import ULID

from app.models import Restaurant


class RestaurantBase(BaseModel):
    owner_id: ULID  # Once auth is operational, move this to RestaurantResponse only (it should not exist in PatchRestaurantRequest) because users should not be able to create restaurants for other users. Derive the owner ID from the authenticated session.
    name: str
    description: str
    address: str
    phone_number: str
    is_active: bool


class PatchRestaurantRequest(BaseModel):
    # This is a separate class to the base class with default constructor arguments, so patch requests only need to contain the fields being updated.

    # No ID needed because it can be passed via the URL.

    owner_id: ULID | None = None  # This allows restaurants to be transferred to other owners post-creation.
    name: str | None = None
    description: str | None = None
    address: str | None = None
    phone_number: str | None = None
    is_active: bool | None = None


class PostRestaurantRequest(RestaurantBase):
    pass

    
class RestaurantResponse(RestaurantBase):
    id: ULID

    def __init__(self, restaurant: Restaurant):
        pass  # Create from restaurant instance.
