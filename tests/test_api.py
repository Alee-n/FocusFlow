import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_health_endpoint():

    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "running"


def test_login_requires_username():

    client = app.test_client()

    response = client.post("/api/login", json={})

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False


def test_login_success():

    client = app.test_client()

    response = client.post("/api/login", json={"username": "lia"})

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assert "access_token" in data
