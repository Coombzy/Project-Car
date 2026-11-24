"""AUD-048: expired login-failure keys are swept on the next reserve."""

from __future__ import annotations

import pytest

from app.auth import (
    _LOGIN_FAILURE_WINDOW_SECONDS,
    _account_failures,
    _login_failures,
    clear_login_failures,
    release_login_failure,
    reserve_login_failure,
)


def test_ten_thousand_expired_clients_are_swept_on_next_reserve(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 5000.0}
    monkeypatch.setattr("app.auth.time.monotonic", lambda: clock["now"])
    clear_login_failures()
    for index in range(10_000):
        reserved = reserve_login_failure(
            f"198.51.{index // 256}.{index % 256}",
            "owner",
            f"sweep{index}@example.com",
        )
        assert reserved is not None
    clock["now"] += _LOGIN_FAILURE_WINDOW_SECONDS + 1
    fresh_ip = "203.0.113.250"
    fresh = reserve_login_failure(fresh_ip, "owner", "fresh-sweep@example.com")
    assert fresh is not None
    release_login_failure(fresh_ip, fresh)
    assert len(_login_failures) == 0
    now = clock["now"]
    expired_accounts = sum(
        1
        for _count, seen in _account_failures.values()
        if now - seen >= _LOGIN_FAILURE_WINDOW_SECONDS
    )
    assert expired_accounts == 0
