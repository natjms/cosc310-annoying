from pydantic import BaseModel

class Restaurant(BaseModel):
    id: str
    name: str
    description: str
    address: str
    phone: str
