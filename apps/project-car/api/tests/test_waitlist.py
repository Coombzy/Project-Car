from __future__ import annotations

from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH


def _allocation_rows(client: TestClient, member_id: str) -> list[dict]:
    listed = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return [row for row in listed.json() if row["kind"] == "monthly_allocation"]


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
    assert login.json()["role"] == "owner"
    assert login.json()["email"] == "owner@projectcar.ca"
    me = client.get("/me")
    assert me.status_code == 200
    listed = client.get("/waitlist")
    assert listed.status_code == 200
    assert listed.json()[0]["email"] == "ben@example.com"


def test_waitlist_convert_creates_member_and_allocation(client: TestClient) -> None:
    created = client.post(
        "/waitlist",
        json={
            "name": "Priya Shah",
            "email": "priya.shah@example.com",
            "phone": "403-555-0188",
            "notes": "Premium interest",
        },
    )
    assert created.status_code == 201, created.text
    entry_id = created.json()["id"]

    tiers = client.get("/tiers", headers=AUTH)
    assert tiers.status_code == 200, tiers.text
    premium = next(row for row in tiers.json() if row["name"] == "premium")
    expected_tokens = Decimal(premium["included_tokens"])

    converted = client.post(
        f"/waitlist/{entry_id}/convert",
        headers=AUTH,
        json={"tier_name": "premium"},
    )
    assert converted.status_code == 200, converted.text
    member_id = converted.json()["member_id"]
    assert member_id

    member = client.get(f"/members/{member_id}", headers=AUTH)
    assert member.status_code == 200, member.text
    body = member.json()
    assert body["email"] == "priya.shah@example.com"
    assert body["name"] == "Priya Shah"
    assert body["phone"] == "403-555-0188"
    assert body["status"] == "active"
    assert body["tier_name"] == "premium"
    assert Decimal(str(body["token_balance"])) == expected_tokens

    grants = _allocation_rows(client, member_id)
    assert len(grants) == 1
    assert Decimal(str(grants[0]["amount"])) == expected_tokens

    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    row = next(item for item in listed.json() if item["id"] == entry_id)
    assert row["member_id"] == member_id

    again = client.post(
        f"/waitlist/{entry_id}/convert",
        headers=AUTH,
        json={"tier_name": "basic"},
    )
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "already_converted"
    assert _allocation_rows(client, member_id) == grants
    members = client.get("/members", headers=AUTH)
    assert members.status_code == 200, members.text
    assert sum(1 for item in members.json() if item["email"] == "priya.shah@example.com") == 1

    existing = client.post(
        "/members",
        headers=AUTH,
        json={
            "name": "Ada Reyes",
            "email": "ada@example.com",
            "phone": "403-555-0100",
            "tier_name": "basic",
        },
    )
    assert existing.status_code == 201, existing.text
    existing_id = existing.json()["id"]
    ada_grants = _allocation_rows(client, existing_id)
    assert len(ada_grants) == 1
    before_members = client.get("/members", headers=AUTH).json()

    duplicate = client.post(
        "/waitlist",
        json={"name": "Ada Two", "email": "ada@example.com", "phone": "403-555-0199"},
    )
    assert duplicate.status_code == 201, duplicate.text
    duplicate_id = duplicate.json()["id"]
    conflict = client.post(
        f"/waitlist/{duplicate_id}/convert",
        headers=AUTH,
        json={"tier_name": "premium"},
    )
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "duplicate_email"
    assert _allocation_rows(client, existing_id) == ada_grants
    after = client.get("/waitlist", headers=AUTH)
    assert after.status_code == 200, after.text
    dup_row = next(item for item in after.json() if item["id"] == duplicate_id)
    assert dup_row["member_id"] is None
    after_members = client.get("/members", headers=AUTH).json()
    assert len(after_members) == len(before_members)
    assert sum(1 for item in after_members if item["email"] == "ada@example.com") == 1
