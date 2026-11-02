from pydantic import BaseModel
from ulid import ULID


class RestaurantBase(BaseModel):
    name: str
    description: str
    address: str
    phone_number: str
    is_active: bool


class PatchRestaurantRequest(BaseModel):
    # This is a separate class to the base class with default constructor arguments, so patch requests only need to contain the fields being updated.

    # No ID needed because it can be passed via the URL.

    name: str | None = None
    owner_id: ULID | None = None  # This allows restaurants to be transferred to other owners post-creation.
    description: str | None = None
    address: str | None = None
    phone_number: str | None = None
    is_active: bool | None = None


class PostRestaurantRequest(RestaurantBase):
    # No owner ID because users should not be able to create restaurants for other users. Derive the owner ID from the authenticated session.
    pass

    
class RestaurantResponse(RestaurantBase):
    id: ULID
    owner_id: ULID
