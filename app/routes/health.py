from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class HealthResponse(BaseModel):
    pass

@router.get('/health', summary='Checks if the API is online and responding')
def get_health() -> HealthResponse:
    """Get the current API health.

    Returns:
        An empty json object.

    """
    return HealthResponse()
