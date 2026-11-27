"""Missing or unknown signup_mode reads as waitlist. Explicit self_serve stays.

Self-serve signup accepts only the stand-in basic tier.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.models import ShopSetting
from app.services.signup_mode import (
    SIGNUP_MODE_KEY,
    SIGNUP_SELF_SERVE,
    SIGNUP_WAITLIST,
    get_signup_mode,
)
from tests.conftest import AUTH
from tests.test_self_serve_signup import _signup

PREMIUM_EMAIL = "premium.self.serve@example.com"


def _session(client: TestClient):
    return client.session_factory()  # type: ignore[attr-defined]


def test_missing_signup_mode_row_is_waitlist(client: TestClient) -> None:
    session = _session(client)
    try:
        assert session.get(ShopSetting, SIGNUP_MODE_KEY) is None
        assert get_signup_mode(session) == SIGNUP_WAITLIST
    finally:
        session.close()

    mode = client.get("/signup-mode")
    assert mode.status_code == 200, mode.text
    assert mode.json()["mode"] == "waitlist"


def test_unknown_signup_mode_value_is_waitlist(client: TestClient) -> None:
    session = _session(client)
    session.add(ShopSetting(key=SIGNUP_MODE_KEY, value="banana"))
    session.commit()
    try:
        assert get_signup_mode(session) == SIGNUP_WAITLIST
    finally:
        session.close()

    mode = client.get("/signup-mode")
    assert mode.status_code == 200, mode.text
    assert mode.json()["mode"] == "waitlist"


def test_explicit_self_serve_row_is_unchanged(client: TestClient) -> None:
    session = _session(client)
    session.add(ShopSetting(key=SIGNUP_MODE_KEY, value=SIGNUP_SELF_SERVE))
    session.commit()
    try:
        stored = session.get(ShopSetting, SIGNUP_MODE_KEY)
        assert stored is not None
        assert stored.value == SIGNUP_SELF_SERVE
        assert get_signup_mode(session) == SIGNUP_SELF_SERVE
    finally:
        session.close()

    mode = client.get("/signup-mode")
    assert mode.status_code == 200, mode.text
    assert mode.json()["mode"] == "self_serve"


def test_self_serve_premium_signup_is_tier_not_self_serve(client: TestClient) -> None:
    switched = client.patch("/signup-mode", headers=AUTH, json={"mode": "self_serve"})
    assert switched.status_code == 200, switched.text
    assert switched.json()["mode"] == "self_serve"

    signed = _signup(client, tier_name="premium", email=PREMIUM_EMAIL)
    assert signed.status_code == 400, signed.text
    assert signed.json()["error"]["code"] == "tier_not_self_serve"
    assert client.cookies.get("pc_member_session") is None

    members = client.get("/members", headers=AUTH)
    assert members.status_code == 200, members.text
    assert all(row["email"] != PREMIUM_EMAIL for row in members.json())


def test_self_serve_basic_signup_still_201(client: TestClient) -> None:
    switched = client.patch("/signup-mode", headers=AUTH, json={"mode": "self_serve"})
    assert switched.status_code == 200, switched.text
    assert switched.json()["mode"] == "self_serve"

    signed = _signup(client, email="basic.self.serve@example.com")
    assert signed.status_code == 201, signed.text
    assert signed.json()["tier_name"] == "basic"
