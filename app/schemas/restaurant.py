from pydantic import BaseModel

from app.models import Restaurant


class PostRestaurantRequest(BaseModel):
    # No owner_id because this should be derived from the session.
    
    name: str
    description: str
    address: str
    phone_number: str
    is_active: bool


class PatchRestaurantRequest(BaseModel):
    # No owner_id because you should not be able to transfer a restaurant to another user. This would be a pain to implement too because the other user would have to be willing to accept it.

    name: str | None = None
    description: str | None = None
    address: str | None = None
    phone_number: str | None = None
    is_active: bool | None = None

    
class RestaurantResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    description: str
    address: str
    phone_number: str
    is_active: bool

    def __init__(self, restaurant: Restaurant):
        raise NotImplementedError()
