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
    cookie_secure: bool = False
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    pc_waitlist: bool = True

    @field_validator("owner_email", mode="before")
    @classmethod
    def normalize_owner_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
