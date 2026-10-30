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

# Profile is a new member nav item. At 390 the nav wraps. At 768 the
# email drops to the next row. A capture can still sit inside the 0.01
# pixel cap, so these member refs are replaced from text before the
# compare. member-profile is new at 390, 768, and 1440. The login shot
# and the owner shots stay as committed. Chromium is installed when
# the headless shell binary is missing.
browser_root="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"
if ! find "$browser_root" -type f -name chrome-headless-shell 2>/dev/null | grep -q .; then
  npx playwright install chromium
fi

ref="$VISUAL/member-nav-ref"
for width in 390 768 1440; do
  mkdir -p "$VISUAL/screenshots/$width"
  for name in member-home member-cameras member-chat member-chat-room member-jobs member-parts member-schedule member-profile; do
    base64 -d "$ref/$width/$name.b64" > "$VISUAL/screenshots/$width/$name.png"
  done
done

npm run build
