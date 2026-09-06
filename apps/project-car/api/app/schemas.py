from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class WaitlistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @field_validator("phone", "notes", mode="before")
    @classmethod
    def empty_optional(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class WaitlistEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    phone: str | None
    notes: str | None
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()


class PrincipalOut(BaseModel):
    role: str
    email: str
