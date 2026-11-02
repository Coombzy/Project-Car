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
    # Empty outside an env file. Startup refuses these unless SHOP_DEV_MODE=1.
    # Loopback is not dev: the tunnel binds 127.0.0.1.
    shop_dev_mode: bool = False
    owner_email: str = "owner@projectcar.ca"
    owner_password: str = ""
    owner_api_secret: str = ""
    ai_api_secret: str = ""
    ai_actor_id: str = "shop-ai"
    session_secret: str = ""
    session_ttl_seconds: int = 86_400
    cookie_name: str = "pc_owner_session"
    member_cookie_name: str = "pc_member_session"
    # Demo Member password stub. Email must match an existing member row.
    # Not OIDC. Staff OIDC can replace this later without rewriting shop tables.
    member_demo_password: str = ""
    # None: Secure outside dev mode. False opts out (local HTTP). True forces Secure.
    cookie_secure: bool | None = None
    # Header that carries the real client address for the login and waitlist caps.
    # Honoured only when the TCP peer is in trusted_proxies. Empty: key on the peer.
    # The supported production value is CF-Connecting-IP. X-Forwarded-For is refused.
    client_ip_header: str = ""
    trusted_proxies: str = "127.0.0.1,::1"
    # Shared with the shop UI. X-Shop-Client-IP is ignored unless this matches.
    shop_proxy_secret: str = ""
    # Legacy public list. Merged into the brochure (no-credential) origins.
    # Explicit allowlist only. Never "*".
    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "https://projectcar.ca,https://www.projectcar.ca"
    )
    cors_public_origins: str = "https://projectcar.ca,https://www.projectcar.ca"
    cors_credentialed_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "https://ops.projectcar.ca,https://app.projectcar.ca"
    )
    pc_waitlist: bool = True
    # Name of the PaymentProcessor implementation. "stand-in" mints STANDIN- ids.
    payment_processor: str = "stand-in"
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
        return _origin_list(self.cors_origins)

    @property
    def cors_public_origin_list(self) -> list[str]:
        """Brochure origins. Waitlist only, and never with credentials."""
        return _origin_list(self.cors_public_origins)

    @property
    def cors_credentialed_origin_list(self) -> list[str]:
        """Shop UI origins that may send cookies."""
        return _origin_list(self.cors_credentialed_origins)

    def cors_origin_kind(self, origin: str) -> str | None:
        """`credentialed` wins when an origin is on both lists."""
        if origin in self.cors_credentialed_origin_list:
            return "credentialed"
        public = set(self.cors_public_origin_list)
        public.update(self.cors_origin_list)
        if origin in public:
            return "public"
        return None


def _origin_list(raw: str) -> list[str]:
    origins: list[str] = []
    for item in raw.split(","):
        origin = item.strip()
        if not origin or origin == "*":
            continue
        origins.append(origin)
    return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
