"""Brochure origins can post to the waitlist. They cannot send credentialed CORS."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import create_app


def _options(client: TestClient, path: str, origin: str, method: str = "GET"):
    return client.options(
        path,
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "content-type",
        },
    )


def test_brochure_origin_gets_no_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    get_settings.cache_clear()
    try:
        with TestClient(create_app()) as client:
            members = _options(client, "/members", "https://projectcar.ca")
            assert members.headers.get("access-control-allow-credentials") is None
            assert members.headers.get("access-control-allow-origin") is None

            waitlist = _options(client, "/waitlist", "https://projectcar.ca", "POST")
            assert waitlist.status_code in {200, 204}
            assert waitlist.headers.get("access-control-allow-origin") == "https://projectcar.ca"
            assert waitlist.headers.get("access-control-allow-credentials") is None

            ops = _options(client, "/members", "https://ops.projectcar.ca")
            assert ops.headers.get("access-control-allow-origin") == "https://ops.projectcar.ca"
            assert ops.headers.get("access-control-allow-credentials") == "true"
    finally:
        get_settings.cache_clear()
