from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_restaurants_is_200():

    response = client.get("/api/restaurants")

    assert response.status_code == 200


def test_get_restaurants_returns_list():

    response = client.get("/api/restaurants")

    assert isinstance(response.json(), list)


def test_get_restaurants_returns_10_restaurants():

    response = client.get("/api/restaurants")

    assert len(response.json()) == 10
    