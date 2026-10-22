from pydantic import BaseModel
from fastapi import APIRouter

health_router = APIRouter()

class HealthResponse(BaseModel):
    pass

@health_router.get('/health', summary='Checks if the API is online and responding')
def get_health() -> HealthResponse:
    """Get the current API health.

    Returns:
        An empty json object.
    """
    return HealthResponse()
