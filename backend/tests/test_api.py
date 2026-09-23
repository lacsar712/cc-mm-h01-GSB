import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def login(client, username, password):
    resp = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_reader_cannot_create_reading(client):
    """只读角色继续写不进去：viewer 上报被 403 拒绝。"""
    token = login(client, "viewer", "view123456")
    resp = client.post(
        "/api/readings",
        headers=auth(token),
        json={"site": "回风巷", "ch4_pct": 1.2},
    )
    assert resp.status_code == 403


def test_writer_alarm_goes_through_to_store_and_list(client):
    """writer 上报踩线值：写入结论、推送载荷、列表行都保持判定函数原话，无旁路字段。"""
    token = login(client, "gasman", "gas123456")

    resp = client.post(
        "/api/readings",
        headers=auth(token),
        json={"site": "边界点", "ch4_pct": 1.0},
    )
    assert resp.status_code == 201
    pushed = resp.json()
    assert pushed["level"] == "报警"
    assert pushed["note"] == "甲烷达到报警线"
    assert "css" not in pushed
    assert "bypass" not in pushed

    rows = client.get("/api/readings", headers=auth(token)).json()
    row = next(r for r in rows if r["site"] == "边界点")
    assert row["level"] == "报警"
    assert row["note"] == "甲烷达到报警线"
    assert "css" not in row
    assert "bypass" not in row
