from fastapi.testclient import TestClient

from flood_api.__main__ import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
