#!/bin/sh
# Build shop-web with the frozen visual clock baked into the client bundle.
set -eu
VISUAL="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
WEB="$(CDPATH= cd -- "$VISUAL/.." && pwd)"
SHOP_NOW="$(tr -d '[:space:]' < "$VISUAL/shop-now.txt")"
export SHOP_NOW
export NEXT_PUBLIC_SHOP_NOW="$SHOP_NOW"
export SHOP_API_URL="${SHOP_API_URL:-http://127.0.0.1:8000}"
cd "$WEB"
npm run build
# Playwright (reuseExistingServer: false) errors when :8000/health already
# answers, so a leftover visual run blocks the next one. Free 8000 and 3000
# after the build, before `npm run visual`. Do not flip reuseExistingServer.
python3 "$VISUAL/free_visual_ports.py"
