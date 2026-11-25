#!/usr/bin/env python3
"""Shop Postgres compose: loopback bind and required password, no default."""
import pathlib
import re
import sys

COMPOSE = pathlib.Path(__file__).with_name("compose.yaml")
BIND = "127.0.0.1:${SHOP_POSTGRES_PORT:-5432}:5432"
PASSWORD = re.compile(r"\$\{SHOP_POSTGRES_PASSWORD:\?[^}]*\}")
DEFAULT = re.compile(r"SHOP_POSTGRES_PASSWORD:-[^\n]+")


def main() -> int:
    text = COMPOSE.read_text()
    if BIND not in text:
        print(f"missing loopback bind {BIND}", file=sys.stderr)
        return 1
    if not PASSWORD.search(text):
        print("SHOP_POSTGRES_PASSWORD must use ${VAR:?msg} with no default", file=sys.stderr)
        return 1
    if DEFAULT.search(text):
        print("SHOP_POSTGRES_PASSWORD must not set a default", file=sys.stderr)
        return 1
    try:
        import yaml
    except ImportError:
        print("ok")
        return 0
    doc = yaml.safe_load(text)
    svc = doc["services"]["shop-postgres"]
    if svc["ports"] != [BIND]:
        print(f"parsed ports {svc['ports']!r}", file=sys.stderr)
        return 1
    pw = svc["environment"]["POSTGRES_PASSWORD"]
    if not PASSWORD.fullmatch(pw):
        print(f"parsed password interpolation {pw!r}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
