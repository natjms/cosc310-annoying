from pydantic import BaseModel
from fastapi import APIRouter

class HealthResponse(BaseModel):
	pass

health_router = APIRouter()

@health_router.get('/health', summary='Check if the API is online and responding')
def get_health() -> HealthResponse:
	return HealthResponse()
