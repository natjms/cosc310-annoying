from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_health_is_200():
	response = client.get('/api/health')
	assert response.status_code == 200
