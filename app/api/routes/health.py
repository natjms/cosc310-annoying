from fastapi import APIRouter

router = APIRouter()

@router.get('/api/health', summary='Check the health of the server')
def get_health():
	return {}
