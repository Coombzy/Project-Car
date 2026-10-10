from __future__ import annotations

import threading
from pathlib import Path

from fastapi.testclient import TestClient

import app.auth as auth
from app.config import get_settings
from app.seed import demo_password_refusal, main

ROOT = Path(__file__).resolve().parents[4]
PUBLIC_DOCS = (
    ROOT / "README.md",
    ROOT / "apps/project-car/web/README.md",
    ROOT / "apps/project-car/api/README.md",
)


def test_demo_password_refused_off_loopback() -> None:
    message = "the seed refuses changeme unless the host is loopback"
    assert demo_password_refusal("projectcar.ca", "changeme") == message
    assert demo_password_refusal("0.0.0.0", "changeme") == message
    assert demo_password_refusal("10.0.0.8", "changeme") == message
    assert demo_password_refusal("ops.projectcar.ca", "changeme") == message


def test_demo_password_allowed_on_loopback() -> None:
    assert demo_password_refusal("127.0.0.1", "changeme") is None
    assert demo_password_refusal("localhost", "changeme") is None
    assert demo_password_refusal("::1", "changeme") is None
    assert demo_password_refusal("  LocalHost  ", "changeme") is None


def test_other_password_allowed_off_loopback() -> None:
    assert demo_password_refusal("projectcar.ca", "a-real-secret") is None


def test_seed_main_refuses_public_host(monkeypatch) -> None:
    monkeypatch.setenv("SHOP_HOST", "projectcar.ca")
    monkeypatch.setenv("OWNER_PASSWORD", "changeme")
    monkeypatch.setenv("MEMBER_DEMO_PASSWORD", "changeme")
    from app.config import get_settings
    import app.config as config

    get_settings.cache_clear()
    monkeypatch.setattr(config, "settings", get_settings())
    assert main([]) == 1


def test_default_api_secrets_refused_off_loopback(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("SHOP_HOST", "127.0.0.1")
    loopback = client.get("/me", headers={"Authorization": "Bearer dev-owner-secret"})
    assert loopback.status_code == 200, loopback.text

    owner_login = client.post(
        "/auth/login",
        json={"email": "owner@projectcar.ca", "password": "changeme"},
    )
    assert owner_login.status_code == 200, owner_login.text
    created = client.post(
        "/members",
        headers={"Authorization": "Bearer dev-owner-secret"},
        json={"name": "Ada Reyes", "email": "ada@example.com", "tier_name": "premium"},
    )
    assert created.status_code == 201, created.text
    member_loopback = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": "changeme"},
    )
    assert member_loopback.status_code == 200, member_loopback.text
    owner_cookie = client.cookies.get("pc_owner_session")
    member_cookie = client.cookies.get("pc_member_session")
    assert owner_cookie
    assert member_cookie

    monkeypatch.setenv("SHOP_HOST", "projectcar.ca")
    client.cookies.clear()
    client.cookies.set("pc_owner_session", owner_cookie)
    replayed_owner = client.get("/me")
    assert replayed_owner.status_code == 503, replayed_owner.text
    assert replayed_owner.json()["error"]["code"] == "insecure_default"

    client.cookies.clear()
    client.cookies.set("pc_member_session", member_cookie)
    replayed_member = client.get("/me")
    assert replayed_member.status_code == 503, replayed_member.text
    assert replayed_member.json()["error"]["code"] == "insecure_default"
    client.cookies.clear()

    owner = client.get("/me", headers={"Authorization": "Bearer dev-owner-secret"})
    assert owner.status_code == 503, owner.text
    assert owner.json()["error"]["code"] == "insecure_default"

    ai = client.get("/me", headers={"Authorization": "Bearer dev-ai-secret"})
    assert ai.status_code == 503, ai.text
    assert ai.json()["error"]["code"] == "insecure_default"

    login = client.post(
        "/auth/login",
        json={"email": "owner@projectcar.ca", "password": "changeme"},
    )
    assert login.status_code == 503, login.text
    assert login.json()["error"]["code"] == "insecure_default"

    member_login = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": "changeme"},
    )
    assert member_login.status_code == 503, member_login.text
    assert member_login.json()["error"]["code"] == "insecure_default"

    wrong = client.get("/me", headers={"Authorization": "Bearer not-the-secret"})
    assert wrong.status_code == 401, wrong.text

    configured = get_settings()
    monkeypatch.setattr(configured, "owner_api_secret", "real-owner-secret")
    monkeypatch.setattr(configured, "ai_api_secret", "real-ai-secret")
    monkeypatch.setattr(configured, "session_secret", "real-session-secret")

    allowed = client.get("/me", headers={"Authorization": "Bearer real-owner-secret"})
    assert allowed.status_code == 200, allowed.text
    assert allowed.json()["role"] == "owner"

    ai_ok = client.get("/me", headers={"Authorization": "Bearer real-ai-secret"})
    assert ai_ok.status_code == 200, ai_ok.text
    assert ai_ok.json()["role"] == "ai"

    signed_in = client.post(
        "/auth/login",
        json={"email": "owner@projectcar.ca", "password": "changeme"},
    )
    assert signed_in.status_code == 200, signed_in.text

    member_ok = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": "changeme"},
    )
    assert member_ok.status_code == 200, member_ok.text
    assert member_ok.json()["role"] == "member"


def test_login_locks_after_repeated_failures(client: TestClient) -> None:
    owner = {"email": "owner@projectcar.ca", "password": "wrong-guess"}
    member = {"email": "nobody@example.com", "password": "wrong-guess"}

    for _ in range(4):
        member_denied = client.post("/auth/member/login", json=member)
        assert member_denied.status_code == 401, member_denied.text
        assert member_denied.json()["error"]["code"] == "invalid_credentials"
        owner_denied = client.post("/auth/login", json=owner)
        assert owner_denied.status_code == 401, owner_denied.text
        assert owner_denied.json()["error"]["code"] == "invalid_credentials"

    locked_owner = client.post("/auth/login", json=owner)
    assert locked_owner.status_code == 429, locked_owner.text
    assert locked_owner.json()["error"]["code"] == "rate_limited"

    locked_member = client.post("/auth/member/login", json=member)
    assert locked_member.status_code == 429, locked_member.text
    assert locked_member.json()["error"]["code"] == "rate_limited"

    still_locked = client.post(
        "/auth/login",
        json={"email": "owner@projectcar.ca", "password": "changeme"},
    )
    assert still_locked.status_code == 429, still_locked.text
    assert still_locked.json()["error"]["code"] == "rate_limited"


def test_overlapping_attempts_cannot_both_pass_one_under_the_cap() -> None:
    """One slot remains. Overlapping attempts must not both clear the guard."""
    ip = "203.0.113.77"
    for _ in range(7):
        auth.record_login_failure(ip)

    start = threading.Barrier(2)
    observed = threading.Barrier(2)
    admitted: list[bool] = []
    record = threading.Lock()

    def attempt() -> None:
        start.wait(timeout=5)
        limited = auth.login_failure_limited(ip)
        observed.wait(timeout=5)
        if not limited:
            auth.record_login_failure(ip)
        with record:
            admitted.append(not limited)

    threads = [threading.Thread(target=attempt) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    assert len(admitted) == 2, admitted
    assert admitted.count(True) == 1, admitted


def test_login_lock_expires_after_fifteen_minutes(monkeypatch) -> None:
    clock = {"now": 10_000.0}
    monkeypatch.setattr(auth.time, "monotonic", lambda: clock["now"])
    ip = "203.0.113.9"
    for _ in range(8):
        assert auth.login_failure_limited(ip) is False
        auth.record_login_failure(ip)
    assert auth.login_failure_limited(ip) is True
    assert auth.login_failure_limited("203.0.113.10") is False
    clock["now"] += 15 * 60
    assert auth.login_failure_limited(ip) is True
    clock["now"] += 1
    assert auth.login_failure_limited(ip) is False


def test_inactive_member_login_matches_unknown_email(client: TestClient) -> None:
    created = client.post(
        "/members",
        headers={"Authorization": "Bearer dev-owner-secret"},
        json={
            "name": "Jordan",
            "email": "jordan@example.com",
            "tier_name": "premium",
            "status": "suspended",
        },
    )
    assert created.status_code == 201, created.text
    inactive = client.post(
        "/auth/member/login",
        json={"email": "jordan@example.com", "password": "changeme"},
    )
    unknown = client.post(
        "/auth/member/login",
        json={"email": "nobody@example.com", "password": "changeme"},
    )
    assert inactive.status_code == 401, inactive.text
    assert unknown.status_code == 401, unknown.text
    assert inactive.json() == unknown.json()
    assert inactive.json()["error"]["code"] == "invalid_credentials"


def test_public_docs_omit_demo_login() -> None:
    docs = list(PUBLIC_DOCS)
    docs.extend((ROOT / "Docs").rglob("*.md"))
    for path in docs:
        text = path.read_text()
        assert "changeme" not in text, path
        assert "owner@projectcar.ca" not in text, path
