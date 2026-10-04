from pydantic import BaseModel

class MenuItem(BaseModel):
	cuisine: str
	name: str
	price: float

class Menu(BaseModel):
	name: str
	items: list[MenuItem]
