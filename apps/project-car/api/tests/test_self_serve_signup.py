"""A new member signs up, sets a password, and picks Basic.

The waitlist stays as the fallback when the owner switches signup mode.
"""

from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH

EMAIL = "self.serve@example.com"
PASSWORD = "walkthrough-pass"


def _signup(client: TestClient, **overrides: object):
    transport = client._transport
    previous = transport.client
    transport.client = ("203.0.113.51", 50000)
    body = {
        "name": "Self Serve",
        "email": EMAIL,
        "phone": "403-555-0199",
        "password": PASSWORD,
        "tier_name": "basic",
    }
    body.update(overrides)
    try:
        return client.post("/signup", json=body)
    finally:
        transport.client = previous


def test_self_serve_signup_picks_basic_and_can_sign_in(client: TestClient) -> None:
    signed = _signup(client)
    assert signed.status_code == 201, signed.text
    body = signed.json()
    assert body["mode"] == "self_serve"
    assert body["tier_name"] == "basic"
    member_id = body["member_id"]

    logged = client.post("/auth/member/login", json={"email": EMAIL, "password": PASSWORD})
    assert logged.status_code == 200, logged.text
    me = client.get("/member/me")
    assert me.status_code == 200, me.text
    assert me.json()["id"] == member_id
    assert me.json()["tier_name"] == "basic"
    assert Decimal(str(me.json()["allowance_balance"])) == Decimal("1000")
    assert Decimal(str(me.json()["token_balance"])) == Decimal("1000")

    waitlist = client.get("/waitlist", headers=AUTH)
    assert waitlist.status_code == 200, waitlist.text
    assert all(row["email"] != EMAIL for row in waitlist.json())


def test_waitlist_is_the_fallback_when_the_owner_switches(client: TestClient) -> None:
    switched = client.patch("/signup-mode", headers=AUTH, json={"mode": "waitlist"})
    assert switched.status_code == 200, switched.text
    assert switched.json()["mode"] == "waitlist"

    signed = _signup(client, email="fallback@example.com", password=None)
    assert signed.status_code == 201, signed.text
    assert signed.json()["mode"] == "waitlist"
    assert signed.json()["member_id"] is None

    members = client.get("/members", headers=AUTH)
    assert members.status_code == 200, members.text
    assert all(row["email"] != "fallback@example.com" for row in members.json())
    waitlist = client.get("/waitlist", headers=AUTH)
    assert any(row["email"] == "fallback@example.com" for row in waitlist.json())

    restored = client.patch("/signup-mode", headers=AUTH, json={"mode": "self_serve"})
    assert restored.status_code == 200, restored.text
