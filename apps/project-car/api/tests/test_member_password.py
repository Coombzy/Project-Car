"""A member with their own password does not accept the shared demo password."""

from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient

from app.config import settings
from app.db import get_db
from app.main import app
from app.models import Member
from app.seed import seed
from tests.conftest import AUTH, create_member, login_member

OWN_PASSWORD = "bay-door-4821"
WRONG_PASSWORD = "not-the-password"
RESET_PASSWORD = "garage-key-991"


def _login(client: TestClient, email: str, password: str):
    return client.post("/auth/member/login", json={"email": email, "password": password})


def _stored_hash(client: TestClient, member_id: str) -> str | None:
    factory = client.session_factory  # type: ignore[attr-defined]
    session = factory()
    try:
        row = session.get(Member, UUID(member_id))
        assert row is not None
        return row.password_hash
    finally:
        session.close()


def test_own_password_refuses_shared_and_is_stored_hashed(client: TestClient) -> None:
    shared = settings.member_demo_password
    assert shared not in {OWN_PASSWORD, WRONG_PASSWORD, RESET_PASSWORD}

    member = create_member(client, email="ada@example.com")
    # No hash yet: today's shared password still signs this member in.
    assert _login(client, member["email"], shared).status_code == 200

    anonymous = client.post(
        f"/members/{member['id']}/password",
        json={"password": OWN_PASSWORD},
    )
    assert anonymous.status_code == 401

    saved = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": OWN_PASSWORD},
    )
    assert saved.status_code == 200, saved.text
    assert OWN_PASSWORD not in saved.text
    assert "password_hash" not in saved.json()

    detail = client.get(f"/members/{member['id']}", headers=AUTH)
    assert detail.status_code == 200
    assert OWN_PASSWORD not in detail.text
    assert "password_hash" not in detail.json()

    shared_denied = _login(client, member["email"], shared)
    assert shared_denied.status_code == 401
    assert shared_denied.json()["error"]["code"] == "invalid_credentials"

    wrong = _login(client, member["email"], WRONG_PASSWORD)
    assert wrong.status_code == 401
    assert wrong.json()["error"]["code"] == "invalid_credentials"

    own = _login(client, member["email"], OWN_PASSWORD)
    assert own.status_code == 200, own.text
    assert own.json()["role"] == "member"
    assert own.json()["email"] == member["email"]

    stored = _stored_hash(client, member["id"])
    assert stored
    assert stored != OWN_PASSWORD
    assert OWN_PASSWORD not in stored

    reset = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": RESET_PASSWORD},
    )
    assert reset.status_code == 200, reset.text
    assert RESET_PASSWORD not in reset.text
    assert _login(client, member["email"], OWN_PASSWORD).status_code == 401
    again = _login(client, member["email"], RESET_PASSWORD)
    assert again.status_code == 200, again.text
    replaced = _stored_hash(client, member["id"])
    assert replaced
    assert replaced != RESET_PASSWORD
    assert RESET_PASSWORD not in replaced
    assert OWN_PASSWORD not in replaced


def _seed_demo(client: TestClient) -> None:
    override = app.dependency_overrides[get_db]
    session_gen = override()
    session = next(session_gen)
    try:
        seed(session, reset=True)
        session.commit()
    finally:
        session_gen.close()


def test_seed_hashes_configured_member_password(client: TestClient, monkeypatch) -> None:
    configured = "correct-horse"
    monkeypatch.setattr(settings, "member_demo_password", configured)
    _seed_demo(client)

    shared = _login(client, "ada.reyes@example.com", "changeme")
    assert shared.status_code == 401
    assert shared.json()["error"] == {
        "code": "invalid_credentials",
        "message": "Email or password is incorrect.",
    }

    signed_in = _login(client, "ada.reyes@example.com", configured)
    assert signed_in.status_code == 200, signed_in.text
    assert signed_in.json()["role"] == "member"
    assert signed_in.json()["email"] == "ada.reyes@example.com"


def test_unknown_email_keeps_the_invalid_credentials_body(client: TestClient) -> None:
    missing = _login(client, "nobody@example.com", "correct-horse")
    assert missing.status_code == 401
    assert missing.json()["error"] == {
        "code": "invalid_credentials",
        "message": "Email or password is incorrect.",
    }


def test_member_session_cannot_set_password(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    login_member(client, member["email"])
    denied = client.post(
        f"/members/{member['id']}/password",
        json={"password": OWN_PASSWORD},
    )
    assert denied.status_code in {401, 403}


def test_personal_password_may_match_shared_demo_password(client: TestClient) -> None:
    shared = settings.member_demo_password
    member = create_member(client, email="riley@example.com")
    saved = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": shared},
    )
    assert saved.status_code == 200, saved.text
    assert shared not in saved.text
    signed_in = _login(client, member["email"], shared)
    assert signed_in.status_code == 200, signed_in.text
    assert signed_in.json()["role"] == "member"


def test_rejected_password_is_not_returned(client: TestClient) -> None:
    member = create_member(client, email="sam@example.com")
    secret = "not-stored-plaintext"
    rejected = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"note": secret},
    )
    assert rejected.status_code == 422
    assert secret not in rejected.text
    assert rejected.json()["error"]["message"] == "Password is required."
