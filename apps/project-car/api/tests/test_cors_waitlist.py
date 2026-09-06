from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import create_app


def test_cors_allowlist_includes_public_site_and_localhost() -> None:
    settings = Settings(
        cors_origins=(
            "http://localhost:3000,http://127.0.0.1:3000,"
            "https://projectcar.ca,https://www.projectcar.ca"
        )
    )
    assert settings.cors_origin_list == [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://projectcar.ca",
        "https://www.projectcar.ca",
    ]


def test_cors_allowlist_drops_wildcard() -> None:
    settings = Settings(cors_origins="https://projectcar.ca, *, http://localhost:3000")
    assert "*" not in settings.cors_origin_list
    assert settings.cors_origin_list == ["https://projectcar.ca", "http://localhost:3000"]


def test_public_waitlist_cors_preflight_and_post(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "http://localhost:3000,https://projectcar.ca,https://www.projectcar.ca",
    )
    get_settings.cache_clear()
    try:
        with TestClient(create_app()) as isolated:
            preflight = isolated.options(
                "/waitlist",
                headers={
                    "Origin": "https://projectcar.ca",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type",
                },
            )
            assert preflight.status_code in {200, 204}
            assert preflight.headers.get("access-control-allow-origin") == "https://projectcar.ca"

            www = isolated.options(
                "/waitlist",
                headers={
                    "Origin": "https://www.projectcar.ca",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type",
                },
            )
            assert www.headers.get("access-control-allow-origin") == "https://www.projectcar.ca"

            denied_origin = isolated.options(
                "/waitlist",
                headers={
                    "Origin": "https://evil.example",
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert denied_origin.headers.get("access-control-allow-origin") != "https://evil.example"
    finally:
        get_settings.cache_clear()


def test_public_waitlist_json_errors_have_code_and_message(client: TestClient) -> None:
    invalid = client.post("/waitlist", json={"name": "", "email": "not-an-email"})
    assert invalid.status_code == 422
    error = invalid.json()["error"]
    assert error["code"] == "validation_error"
    assert error["message"]

    client.post("/waitlist", json={"name": "Ada", "email": "ada@example.com"})
    duplicate = client.post("/waitlist", json={"name": "Ada Two", "email": "ADA@example.com"})
    assert duplicate.status_code == 409
    assert duplicate.json()["error"] == {
        "code": "duplicate_email",
        "message": "That email is already on the waitlist.",
    }
