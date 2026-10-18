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
