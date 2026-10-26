from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def login(username, password):
    return client.post("/login", json={"username": username, "password": password})


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_bad_login():
    assert login("emp_user", "wrong").status_code == 401


def test_chat_requires_token():
    assert client.post("/chat", json={"question": "hi"}).status_code in (401, 403)


def test_fake_token_rejected():
    r = client.post("/chat", json={"question": "hi"}, headers=auth("fake.token.value"))
    assert r.status_code == 401


def test_employee_cannot_see_marketing():
    token = login("emp_user", "employee123").json()["access_token"]
    r = client.post("/chat", json={"question": "Marketing report Q3 2024?"}, headers=auth(token))
    assert r.status_code == 200
    assert all(s["department"] == "general" for s in r.json()["sources"])


def test_marketing_user_sees_marketing():
    token = login("mkt_user", "marketing123").json()["access_token"]
    r = client.post("/chat", json={"question": "Marketing report Q3 2024?"}, headers=auth(token))
    assert any(s["department"] == "marketing" for s in r.json()["sources"])