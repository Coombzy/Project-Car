"""AUD-007: /me stays 200 when cookie names come from settings."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from tests.conftest import create_member

OWNER = "custom_owner_cookie"
MEMBER = "custom_member_cookie"


def test_me_follows_cookie_names_from_settings(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "cookie_name", OWNER)
    monkeypatch.setattr(settings, "member_cookie_name", MEMBER)

    owner = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": settings.owner_password},
    )
    assert owner.status_code == 200, owner.text
    assert client.cookies.get(OWNER)
    assert client.cookies.get("pc_owner_session") is None
    me = client.get("/me")
    assert me.status_code == 200, me.text
    assert me.json()["role"] == "owner"

    client.cookies.clear()
    create_member(client)
    member = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": settings.member_demo_password},
    )
    assert member.status_code == 200, member.text
    assert client.cookies.get(MEMBER)
    assert client.cookies.get("pc_member_session") is None
    me = client.get("/me")
    assert me.status_code == 200, me.text
    assert me.json()["role"] == "member"
