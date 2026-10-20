"""A member with their own password does not accept the shared demo password."""

from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient
from itsdangerous import URLSafeTimedSerializer

from app.auth import MEMBER_SALT
from app.config import get_settings, settings
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


def test_unhashed_member_default_password_refused_off_loopback(
    client: TestClient, monkeypatch
) -> None:
    """Off loopback, a new member with no hash cannot sign in with changeme.

    The 401 body matches a wrong password. A non-default shared password still
    works. Loopback demo login and a member who has their own hash stay as they are.
    """
    live = get_settings()
    monkeypatch.setenv("SHOP_HOST", "127.0.0.1")
    monkeypatch.setattr(live, "member_demo_password", "changeme")
    member = create_member(client, email="new.member@example.com")
    assert _stored_hash(client, member["id"]) is None

    # Real session secret so the login is not refused as an insecure dev default.
    # Patch the cached Settings object the login route reads. A prior test may
    # have cleared get_settings(), so the imported settings singleton can differ.
    monkeypatch.setattr(live, "session_secret", "real-session-secret")
    monkeypatch.setenv("SHOP_HOST", "projectcar.ca")

    wrong = _login(client, member["email"], WRONG_PASSWORD)
    assert wrong.status_code == 401, wrong.text
    assert wrong.json()["error"] == {
        "code": "invalid_credentials",
        "message": "Email or password is incorrect.",
    }

    refused = _login(client, member["email"], "changeme")
    assert refused.status_code == 401, refused.text
    assert refused.json() == wrong.json()

    monkeypatch.setattr(live, "member_demo_password", "shop-floor-shared")
    signed_in = _login(client, member["email"], "shop-floor-shared")
    assert signed_in.status_code == 200, signed_in.text
    assert signed_in.json()["role"] == "member"
    assert signed_in.json()["email"] == member["email"]
    still_default = _login(client, member["email"], "changeme")
    assert still_default.status_code == 401, still_default.text
    assert still_default.json() == wrong.json()

    monkeypatch.setattr(live, "member_demo_password", "changeme")
    monkeypatch.setenv("SHOP_HOST", "127.0.0.1")
    loopback = _login(client, member["email"], "changeme")
    assert loopback.status_code == 200, loopback.text
    assert loopback.json()["role"] == "member"

    saved = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": OWN_PASSWORD},
    )
    assert saved.status_code == 200, saved.text
    monkeypatch.setenv("SHOP_HOST", "ops.projectcar.ca")
    shared_denied = _login(client, member["email"], "changeme")
    assert shared_denied.status_code == 401, shared_denied.text
    assert shared_denied.json()["error"]["code"] == "invalid_credentials"
    own = _login(client, member["email"], OWN_PASSWORD)
    assert own.status_code == 200, own.text
    assert own.json()["role"] == "member"

    monkeypatch.setenv("SHOP_HOST", "127.0.0.1")
    hashed_default = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": "changeme"},
    )
    assert hashed_default.status_code == 200, hashed_default.text
    monkeypatch.setenv("SHOP_HOST", "projectcar.ca")
    own_default = _login(client, member["email"], "changeme")
    assert own_default.status_code == 200, own_default.text
    assert own_default.json()["role"] == "member"


def _member_session_claims(token: str) -> dict:
    claims = URLSafeTimedSerializer(settings.session_secret, salt=MEMBER_SALT).loads(token)
    assert isinstance(claims, dict)
    return claims


def _replay_member_cookie(client: TestClient, token: str) -> None:
    client.cookies.clear()
    client.cookies.set("pc_member_session", token)


def test_password_change_revokes_old_member_session(client: TestClient) -> None:
    """A cookie from before the password change is 401. A new login works.

    Covers an unset hash and a later reset. The cookie may carry a short
    fingerprint. It must not carry the password or the stored hash.
    """
    member = create_member(client, email="ada@example.com")
    signed_in = _login(client, member["email"], settings.member_demo_password)
    assert signed_in.status_code == 200, signed_in.text
    assert client.get("/member/me").status_code == 200

    old_cookie = client.cookies.get("pc_member_session")
    assert old_cookie
    owner = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": settings.owner_password},
    )
    assert owner.status_code == 200, owner.text
    owner_cookie = client.cookies.get("pc_owner_session")
    assert owner_cookie

    saved = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": OWN_PASSWORD},
    )
    assert saved.status_code == 200, saved.text
    assert OWN_PASSWORD not in saved.text

    _replay_member_cookie(client, old_cookie)
    stale = client.get("/member/me")
    assert stale.status_code == 401, stale.text
    assert stale.json()["error"] == {
        "code": "unauthorized",
        "message": "Member authentication required.",
    }
    stale_me = client.get("/me")
    assert stale_me.status_code == 401, stale_me.text

    client.cookies.clear()
    client.cookies.set("pc_owner_session", owner_cookie)
    owner_still = client.get("/me")
    assert owner_still.status_code == 200, owner_still.text
    assert owner_still.json()["role"] == "owner"

    client.cookies.clear()
    fresh = _login(client, member["email"], OWN_PASSWORD)
    assert fresh.status_code == 200, fresh.text
    current = client.get("/member/me")
    assert current.status_code == 200, current.text
    assert current.json()["id"] == member["id"]

    stored = _stored_hash(client, member["id"])
    assert stored
    fresh_cookie = client.cookies.get("pc_member_session")
    assert fresh_cookie
    assert fresh_cookie != old_cookie
    assert OWN_PASSWORD not in fresh_cookie
    assert stored not in fresh_cookie
    fingerprint = _member_session_claims(fresh_cookie)["pwd_fp"]
    assert isinstance(fingerprint, str)
    assert fingerprint != "none"
    assert fingerprint != stored
    assert stored not in fingerprint
    assert "scrypt" not in fingerprint
    assert OWN_PASSWORD not in fingerprint
    assert len(fingerprint) <= 16

    reset_cookie = fresh_cookie
    reset = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": RESET_PASSWORD},
    )
    assert reset.status_code == 200, reset.text
    assert RESET_PASSWORD not in reset.text
    _replay_member_cookie(client, reset_cookie)
    reset_stale = client.get("/member/me")
    assert reset_stale.status_code == 401, reset_stale.text
    assert reset_stale.json()["error"]["message"] == "Member authentication required."

    client.cookies.clear()
    again = _login(client, member["email"], RESET_PASSWORD)
    assert again.status_code == 200, again.text
    restored = client.get("/member/me")
    assert restored.status_code == 200, restored.text
    assert restored.json()["id"] == member["id"]
