#!/bin/sh
# Seed the demo shop on sqlite and serve it for the visual check.
# SHOP_NOW is the frozen clock in visual/shop-now.txt. Loopback only.
set -eu
VISUAL="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
API="$(CDPATH= cd -- "$VISUAL/../../api" && pwd)"
SHOP_NOW="$(tr -d '[:space:]' < "$VISUAL/shop-now.txt")"
export SHOP_NOW
export DATABASE_URL="${DATABASE_URL:-sqlite:////tmp/shop-visual.db}"
export SHOP_HOST="${SHOP_HOST:-127.0.0.1}"
# local dev only — the visual API boots with the demo secrets.
export SHOP_DEV_MODE="${SHOP_DEV_MODE:-1}"
export OWNER_PASSWORD="${OWNER_PASSWORD:-changeme}"
export OWNER_API_SECRET="${OWNER_API_SECRET:-dev-owner-secret}"
export AI_API_SECRET="${AI_API_SECRET:-dev-ai-secret}"
export SESSION_SECRET="${SESSION_SECRET:-dev-session-secret-change-me}"
export MEMBER_DEMO_PASSWORD="${MEMBER_DEMO_PASSWORD:-changeme}"
export COOKIE_SECURE="${COOKIE_SECURE:-false}"
cd "$API"
rm -f /tmp/shop-visual.db /tmp/shop-visual.db-journal /tmp/shop-visual.db-wal /tmp/shop-visual.db-shm
PYTHONPATH="$API${PYTHONPATH:+:$PYTHONPATH}" python3 - <<'PY'
from app.db import engine
from app.models import Base

Base.metadata.create_all(engine)
PY
PYTHONPATH="$API${PYTHONPATH:+:$PYTHONPATH}" python3 -m app.seed --reset
exec env PYTHONPATH="$API${PYTHONPATH:+:$PYTHONPATH}" python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
