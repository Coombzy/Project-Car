"""Every Settings field must have an assignment line in .env.example.

pydantic-settings uses the field name in upper case and no extra prefix
(shop_dev_mode is SHOP_DEV_MODE). Properties and validators are not fields.
SHOP_HOST is not a Settings field and is not required here.
"""

from pathlib import Path

from app.config import Settings

ENV_EXAMPLE = Path(__file__).resolve().parents[1] / ".env.example"


def _assignment_names(text: str) -> set[str]:
    names: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        names.add(line.split("=", 1)[0].strip())
    return names


def test_every_settings_field_has_an_env_example_line() -> None:
    present = _assignment_names(ENV_EXAMPLE.read_text(encoding="utf-8"))
    missing = sorted(
        name for name in Settings.model_fields if name.upper() not in present
    )
    assert missing == [], (
        "Settings fields missing from .env.example: "
        + ", ".join(f"{name} -> {name.upper()}" for name in missing)
    )
