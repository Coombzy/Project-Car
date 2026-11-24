"""Missing or unknown signup_mode reads as waitlist. Explicit self_serve stays."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.models import ShopSetting
from app.services.signup_mode import (
    SIGNUP_MODE_KEY,
    SIGNUP_SELF_SERVE,
    SIGNUP_WAITLIST,
    get_signup_mode,
)


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
