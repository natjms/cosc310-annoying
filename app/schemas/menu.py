from pydantic import BaseModel

class Menu(BaseModel):
	id: str
	name: str
