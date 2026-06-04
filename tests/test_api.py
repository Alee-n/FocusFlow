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

def test_health_response_contains_message():

    client = app.test_client()

    response = client.get("/api/health")

    data = response.get_json()

    assert "message" in data


def test_login_returns_token():

    client = app.test_client()

    response = client.post(
        "/api/login",
        json={"username": "lia"}
    )

    data = response.get_json()

    assert "access_token" in data


def test_login_missing_payload():

    client = app.test_client()

    response = client.post(
        "/api/login",
        json={}
    )

    assert response.status_code == 400


def test_login_invalid_content_type():

    client = app.test_client()

    response = client.post(
        "/api/login"
    )

    assert response.status_code in [400, 415, 500]


def test_admin_without_token():

    client = app.test_client()

    response = client.get("/api/admin")

    assert response.status_code in [401, 422]