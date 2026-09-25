from fastapi import APIRouter

from .health import health_router

api_router = APIRouter(prefix='/api')

api_router.include_router(health_router)
