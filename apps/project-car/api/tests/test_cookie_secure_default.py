"""cookie_secure defaults to True unless SHOP_DEV_MODE=1 or COOKIE_SECURE=false."""

import pytest

from app.config import Settings, get_settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for name in ("SHOP_DEV_MODE", "COOKIE_SECURE"):
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.mark.parametrize(
    ("env", "expected"),
    [({}, True),
     ({"SHOP_DEV_MODE": "1"}, False),
     ({"SHOP_DEV_MODE": "1", "COOKIE_SECURE": "true"}, True),
     ({"COOKIE_SECURE": "false"}, False)],
)
def test_default(monkeypatch, env, expected):
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    assert Settings().cookie_secure is expected
    get_settings.cache_clear()
    assert get_settings().cookie_secure is expected
