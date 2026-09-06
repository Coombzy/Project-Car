from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
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
    owner_password: str = "changeme"
    owner_api_secret: str = "dev-owner-secret"
    session_secret: str = "dev-session-secret-change-me"
    session_ttl_seconds: int = 86_400
    cookie_name: str = "pc_owner_session"
    member_cookie_name: str = "pc_member_session"
    # Demo Member password stub. Email must match an existing member row.
    # Not OIDC. Staff OIDC can replace this later without rewriting shop tables.
    member_demo_password: str = "changeme"
    cookie_secure: bool = False
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
