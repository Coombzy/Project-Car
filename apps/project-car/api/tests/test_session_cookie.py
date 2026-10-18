from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from tests.conftest import create_member


def _set_cookie_headers(response) -> list[str]:
    return response.headers.get_list("set-cookie")


def _cookie_named(response, name: str) -> str:
    matches = [header for header in _set_cookie_headers(response) if header.startswith(f"{name}=")]
    assert len(matches) == 1, _set_cookie_headers(response)
    return matches[0]


def _attrs(header: str) -> dict[str, str | bool]:
    attrs: dict[str, str | bool] = {}
    for part in header.split(";")[1:]:
        item = part.strip()
        if not item:
            continue
        if "=" in item:
            key, _, value = item.partition("=")
            attrs[key.lower()] = value
        else:
            attrs[item.lower()] = True
    return attrs


def test_logout_sets_secure_cookie_when_configured(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Logout Set-Cookie uses the same name, path, and Secure flag as login."""
    settings = get_settings()
    monkeypatch.setattr(settings, "cookie_secure", True)

    owner_login = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": settings.owner_password},
    )
    assert owner_login.status_code == 200, owner_login.text
    owner_set = _attrs(_cookie_named(owner_login, settings.cookie_name))
    assert owner_set.get("path") == "/"
    assert owner_set.get("secure") is True

    owner_logout = client.post("/auth/logout")
    assert owner_logout.status_code == 200, owner_logout.text
    owner_clear = _attrs(_cookie_named(owner_logout, settings.cookie_name))
    assert owner_clear.get("path") == owner_set.get("path")
    assert owner_clear.get("secure") is True
    assert owner_clear.get("max-age") == "0"

    create_member(client)
    member_login = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": settings.member_demo_password},
    )
    assert member_login.status_code == 200, member_login.text
    member_set = _attrs(_cookie_named(member_login, settings.member_cookie_name))
    assert member_set.get("path") == "/"
    assert member_set.get("secure") is True

    member_logout = client.post("/auth/member/logout")
    assert member_logout.status_code == 200, member_logout.text
    member_clear = _attrs(_cookie_named(member_logout, settings.member_cookie_name))
    assert member_clear.get("path") == member_set.get("path")
    assert member_clear.get("secure") is True
    assert member_clear.get("max-age") == "0"


def test_logout_clears_cookie_when_secure_is_false(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Loopback demo (cookie_secure false) still expires the session cookies."""
    settings = get_settings()
    monkeypatch.setattr(settings, "cookie_secure", False)

    owner_login = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": settings.owner_password},
    )
    assert owner_login.status_code == 200, owner_login.text
    owner_set = _attrs(_cookie_named(owner_login, settings.cookie_name))
    assert "secure" not in owner_set

    owner_logout = client.post("/auth/logout")
    assert owner_logout.status_code == 200, owner_logout.text
    owner_header = _cookie_named(owner_logout, settings.cookie_name)
    owner_clear = _attrs(owner_header)
    assert owner_header.startswith(f"{settings.cookie_name}=")
    assert owner_clear.get("path") == "/"
    assert "secure" not in owner_clear
    assert owner_clear.get("max-age") == "0"

    create_member(client)
    member_login = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": settings.member_demo_password},
    )
    assert member_login.status_code == 200, member_login.text
    member_logout = client.post("/auth/member/logout")
    assert member_logout.status_code == 200, member_logout.text
    member_header = _cookie_named(member_logout, settings.member_cookie_name)
    member_clear = _attrs(member_header)
    assert member_header.startswith(f"{settings.member_cookie_name}=")
    assert member_clear.get("path") == "/"
    assert "secure" not in member_clear
    assert member_clear.get("max-age") == "0"
