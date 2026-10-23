from pydantic import BaseModel
from ulid import ULID


class Address(BaseModel):
    name: str = ""
    street: str = ""
    unit: str = ""
    city: str = ""
    province: str = ""
    zip_code: str = ""


class Restaurant(BaseModel):
    id: ULID
    owner_id: ULID
    name: str
    description: str = ""
    address: Address = Address()
    phone_number: str = ""
    is_active: bool = True
    cuisine_ids: set[ULID] = set()


class PostRestaurantRequest(BaseModel):
    owner_id: str
    name: str


class PatchRestaurantRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    phone_number: str | None = None
