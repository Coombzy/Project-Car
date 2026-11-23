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
    ai_api_secret: str = "dev-ai-secret"
    ai_actor_id: str = "shop-ai"
    session_secret: str = "dev-session-secret-change-me"
    session_ttl_seconds: int = 86_400
    cookie_name: str = "pc_owner_session"
    member_cookie_name: str = "pc_member_session"
    # Demo Member password stub. Email must match an existing member row.
    # Not OIDC. Staff OIDC can replace this later without rewriting shop tables.
    member_demo_password: str = "changeme"
    cookie_secure: bool = False
    # Header that carries the real client address for the login and waitlist caps.
    # Empty: key on the TCP peer. No header name is hard-coded.
    client_ip_header: str = ""
    # Explicit allowlist only. Never "*". Public waitlist POSTs need the brochure origins.
    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "https://projectcar.ca,https://www.projectcar.ca"
    )
    # Brochure origins: preflight and POST /waitlist only, never credentialed.
    cors_public_origins: str = "https://projectcar.ca,https://www.projectcar.ca"
    # Ops, app and local dev origins: full credentialed CORS.
    cors_credentialed_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "https://ops.projectcar.ca,https://app.projectcar.ca"
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

    @staticmethod
    def _split_origins(value: str) -> list[str]:
        """Comma-separated origins. `*` is dropped so the API is never wide open."""
        return [origin for origin in (item.strip() for item in value.split(",")) if origin and origin != "*"]

    @property
    def cors_origin_list(self) -> list[str]:
        return self._split_origins(self.cors_origins)

    @property
    def cors_public_origin_list(self) -> list[str]:
        return self._split_origins(self.cors_public_origins) + self.cors_origin_list

    @property
    def cors_credentialed_origin_list(self) -> list[str]:
        return self._split_origins(self.cors_credentialed_origins)

    def cors_origin_kind(self, origin: str) -> str | None:
        """Credentialed wins when an origin appears on both lists."""
        if origin in self.cors_credentialed_origin_list:
            return "credentialed"
        return "public" if origin in self.cors_public_origin_list else None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
