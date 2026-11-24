from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the shop API. Secrets come from the environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(
        default="postgresql+psycopg://projectcar:projectcar@localhost:5432/projectcar",
        description="SQLAlchemy URL for shop Postgres (never Nextcloud MariaDB).",
    )
    owner_email: str = "owner@projectcar.ca"
    # Local dev only: allows the placeholder secrets below and serves the docs routes.
    shop_dev_mode: bool = False
    owner_password: str = "changeme"
    owner_api_secret: str = "dev-owner-secret"
    ai_api_secret: str = "dev-ai-secret"
    ai_actor_id: str = "shop-ai"
    session_secret: str = "dev-session-secret-change-me"
    session_ttl_seconds: int = 86_400
    cookie_name: str = "pc_owner_session"
    member_cookie_name: str = "pc_member_session"
    # Demo Member password stub. Email must match an existing member row.
    # Not OIDC. Staff OIDC can replace this later without rewriting shop tables.
    member_demo_password: str = "changeme"
    # Local dev only. Clears cookie_secure below; no other behavior lives here.
    shop_dev_mode: bool = False
    cookie_secure: bool | None = None  # None: resolved from shop_dev_mode below
    # Header that carries the real client address for the login and waitlist caps.
    # Empty: key on the TCP peer. No header name is hard-coded.
    client_ip_header: str = ""
    # Explicit allowlist only. Never "*". Public waitlist POSTs need the brochure origins.
    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "https://projectcar.ca,https://www.projectcar.ca"
    )
    pc_waitlist: bool = True
    # Next-day fill-the-gaps defaults (America/Regina). Owner can override per send.
    fill_min_discount_pct: float = 10
    fill_max_discount_pct: float = 25
    fill_day_start: str = "08:00"
    fill_day_end: str = "21:00"
    # Only "stand-in" is registered. PAYMENT_PROCESSOR overrides this field.
    # The stand-in does not call a processor and does not apply a fee rate.
    payment_processor: str = "stand-in"
    # Email outbox. Empty SMTP_HOST uses the durable stub (records sent, no network).
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from: str = "shop@projectcar.ca"
    smtp_use_tls: bool = True
    # Google Calendar OAuth scaffold. Empty = Connect Google stays a stub.
    google_oauth_client_id: str = ""
    google_oauth_client_secret: str = ""
    google_oauth_redirect_uri: str = ""

    @field_validator("owner_email", mode="before")
    @classmethod
    def normalize_owner_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @model_validator(mode="after")
    def resolve_cookie_secure(self) -> "Settings":
        if self.cookie_secure is None:
            self.cookie_secure = not self.shop_dev_mode
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        """Comma-separated origins. `*` is dropped so the API is never wide open."""
        origins: list[str] = []
        for item in self.cors_origins.split(","):
            origin = item.strip()
            if not origin or origin == "*":
                continue
            origins.append(origin)
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


# Placeholder secrets that must never boot outside local dev.
_DEMO_SECRETS = ("dev-owner-secret", "dev-ai-secret", "dev-session-secret-change-me", "changeme")


def assert_runtime_secrets(settings: Settings) -> None:
    """Refuse to start on placeholder secrets unless SHOP_DEV_MODE=1. Never names the value."""
    if settings.shop_dev_mode:
        return
    for name, length in (
        ("owner_api_secret", 32), ("ai_api_secret", 32),
        ("session_secret", 32), ("owner_password", 12), ("member_demo_password", 12),
    ):
        value = getattr(settings, name)
        if len(value) < length or value in _DEMO_SECRETS or value.startswith("CHANGE_ME"):
            raise RuntimeError(
                f"Refusing to start: {name} is a placeholder or too short. "
                "Set a real value, or SHOP_DEV_MODE=1 for local dev only."
            )
