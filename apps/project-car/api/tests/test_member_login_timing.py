"""Member login pays one scrypt for unknown, unhashed, and hashed emails."""

from __future__ import annotations

import hashlib
from uuid import UUID

from fastapi.testclient import TestClient

from app.auth import hash_password
from app.models import Member
from tests.conftest import create_member

_OWN_PASSWORD = "own-password-ok"
_WRONG_PASSWORD = "wrong-password"


def _login(client: TestClient, email: str, password: str):
    return client.post("/auth/member/login", json={"email": email, "password": password})


def _set_password_hash(client: TestClient, member_id: str, password: str) -> None:
    factory = client.session_factory  # type: ignore[attr-defined]
    with factory() as session:
        row = session.get(Member, UUID(member_id))
        assert row is not None
        row.password_hash = hash_password(password)
        session.commit()


class _ScryptCounter:
    def __init__(self) -> None:
        self.calls = 0
        self._real = hashlib.scrypt

    def install(self, monkeypatch) -> None:
        real = self._real

        def wrapped(*args, **kwargs):
            self.calls += 1
            return real(*args, **kwargs)

        monkeypatch.setattr(hashlib, "scrypt", wrapped)


def test_scrypt_call_counts(client: TestClient, monkeypatch) -> None:
    """Unknown, unhashed, and hashed members each make exactly one scrypt call.

    Loopback still accepts the shared demo password for an unhashed member and
    rejects a wrong password. A stored hash still rejects that shared password.
    """
    unhashed = create_member(client, email="unhashed@example.com")
    hashed = create_member(client, email="hashed@example.com")
    _set_password_hash(client, hashed["id"], _OWN_PASSWORD)

    counter = _ScryptCounter()
    counter.install(monkeypatch)

    unknown = _login(client, "nobody@example.com", _WRONG_PASSWORD)
    assert unknown.status_code == 401
    assert counter.calls == 1

    counter.calls = 0
    accepted = _login(client, unhashed["email"], "changeme")
    assert accepted.status_code == 200
    assert counter.calls == 1

    counter.calls = 0
    rejected = _login(client, unhashed["email"], _WRONG_PASSWORD)
    assert rejected.status_code == 401
    assert counter.calls == 1

    counter.calls = 0
    own = _login(client, hashed["email"], _OWN_PASSWORD)
    assert own.status_code == 200
    assert counter.calls == 1

    counter.calls = 0
    shared_denied = _login(client, hashed["email"], "changeme")
    assert shared_denied.status_code == 401
    assert counter.calls == 1
