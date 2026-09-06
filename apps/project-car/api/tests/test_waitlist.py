from __future__ import annotations

from fastapi.testclient import TestClient


def test_public_waitlist_create_and_owner_list(client: TestClient) -> None:
    created = client.post(
        "/waitlist",
        json={
            "name": "Ada Owner",
            "email": "ada@example.com",
            "phone": "403-555-0100",
            "notes": "2-post hoist access",
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["email"] == "ada@example.com"
    assert body["name"] == "Ada Owner"
    assert body["phone"] == "403-555-0100"
    assert "created_at" in body

    denied = client.get("/waitlist")
    assert denied.status_code == 401
    assert denied.json()["error"]["code"] == "unauthorized"

    listed = client.get("/waitlist", headers={"Authorization": "Bearer dev-owner-secret"})
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["email"] == "ada@example.com"


def test_waitlist_duplicate_email_conflict(client: TestClient) -> None:
    payload = {"name": "Ada", "email": "ada@example.com"}
    assert client.post("/waitlist", json=payload).status_code == 201
    again = client.post("/waitlist", json={"name": "Ada Two", "email": "ADA@example.com"})
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "duplicate_email"


def test_waitlist_validation_error_shape(client: TestClient) -> None:
    response = client.post("/waitlist", json={"name": "", "email": "not-an-email"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_owner_login_cookie_lists_waitlist(client: TestClient) -> None:
    client.post("/waitlist", json={"name": "Ben", "email": "ben@example.com"})
    login = client.post(
        "/auth/login",
        json={"email": "owner@projectcar.ca", "password": "changeme"},
    )
    assert login.status_code == 200
    assert login.json() == {"role": "owner", "email": "owner@projectcar.ca"}
    me = client.get("/me")
    assert me.status_code == 200
    listed = client.get("/waitlist")
    assert listed.status_code == 200
    assert listed.json()[0]["email"] == "ben@example.com"
