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
    cuisine_ids: set[ULID] = set()

    name: str
    description: str = ""

    address: Address = Address()
    phone_number: str = ""

    is_active: bool = True
