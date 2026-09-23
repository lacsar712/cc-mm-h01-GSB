from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def login(username: str, password: str) -> str:
    resp = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_reader_cannot_create_reading():
    token = login("viewer", "view123456")
    resp = client.post(
        "/api/readings",
        headers={"Authorization": f"Bearer {token}"},
        json={"site": "回风巷", "ch4_pct": 1.4},
    )
    assert resp.status_code == 403


def test_anonymous_cannot_create_reading():
    resp = client.post(
        "/api/readings",
        json={"site": "回风巷", "ch4_pct": 1.4},
    )
    assert resp.status_code == 401
