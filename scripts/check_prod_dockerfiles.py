#!/usr/bin/env python3
"""Prod image Dockerfiles must exist and end on a non-root USER."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = ROOT / "apps/project-car/api/Dockerfile"
WEB = ROOT / "apps/project-car/web/Dockerfile"


def last_user(text: str) -> str | None:
    found = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if parts[0].upper() == "USER" and len(parts) > 1:
            found = parts[1]
    return found


def is_root(user: str | None) -> bool:
    if not user:
        return True
    name = user.split(":", 1)[0]
    return name == "0" or name.lower() == "root"


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in (API, WEB) if not path.is_file()]
    if missing:
        print("missing " + ", ".join(missing), file=sys.stderr)
        return 1
    api = API.read_text()
    web = WEB.read_text()
    if is_root(last_user(api)) or is_root(last_user(web)):
        print("last USER is missing or root", file=sys.stderr)
        return 1
    if "uvicorn" not in api.lower() or "alembic" not in api.lower():
        print("api Dockerfile must mention uvicorn and alembic", file=sys.stderr)
        return 1
    if "next" not in web.lower():
        print("web Dockerfile must mention next", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
