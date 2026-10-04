from __future__ import annotations

from pathlib import Path

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


def test_public_docs_omit_demo_login() -> None:
    docs = list(PUBLIC_DOCS)
    docs.extend((ROOT / "Docs").rglob("*.md"))
    for path in docs:
        text = path.read_text()
        assert "changeme" not in text, path
        assert "owner@projectcar.ca" not in text, path
