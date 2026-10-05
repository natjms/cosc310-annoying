from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_menus_for_restaurant():
	response = client.get('/api/menu/1')
	assert response.status_code == 200
	assert len(response.json()) == 1
	assert response.json()[0]['name'] == 'Test Menu'

def test_get_menus_for_nonexistant_restaurant():
	response = client.get('/api/menu/999999999999999')
	assert response.status_code == 404
	assert 'message' in response.json()
