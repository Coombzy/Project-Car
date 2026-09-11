#!/usr/bin/env bash
# Worker html/_redirects must stay thin: /chat and /chat.html → contact.html only.
# /, /shop, /shop/, /shop.html belong to the Zone 10×301 Option A pack — not this file.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="${1:-$ROOT/html/_redirects}"

if [[ ! -f "$FILE" ]]; then
  echo "error: missing $FILE" >&2
  exit 1
fi

fail=0
line_no=0

is_forbidden_source() {
  case "$1" in
    /|/shop|/shop/|/shop.html) return 0 ;;
    *) return 1 ;;
  esac
}

is_allowed_chat_source() {
  case "$1" in
    /chat|/chat.html) return 0 ;;
    *) return 1 ;;
  esac
}

is_contact_dest() {
  case "$1" in
    /contact.html|contact.html) return 0 ;;
    *) return 1 ;;
  esac
}

while IFS= read -r raw || [[ -n "$raw" ]]; do
  line_no=$((line_no + 1))
  line="${raw%$'\r'}"
  line="${line#"${line%%[![:space:]]*}"}"
  [[ -z "$line" || "$line" == \#* ]] && continue

  read -r src dest code _ <<< "$line"

  if is_forbidden_source "$src"; then
    echo "error: $FILE:$line_no forbidden source '$src' (Zone 10×301 Option A pack owns this route)" >&2
    fail=1
    continue
  fi

  if ! is_allowed_chat_source "$src"; then
    echo "error: $FILE:$line_no source '$src' is not allowed (only /chat and /chat.html → contact.html)" >&2
    fail=1
    continue
  fi

  if ! is_contact_dest "$dest"; then
    echo "error: $FILE:$line_no '$src' must target contact.html (got '${dest:-}')" >&2
    fail=1
    continue
  fi

  if [[ -n "${code:-}" && "$code" != "301" ]]; then
    echo "error: $FILE:$line_no '$src' must be 301 (got '$code')" >&2
    fail=1
  fi
done < "$FILE"

if [[ "$fail" -ne 0 ]]; then
  echo "error: Worker _redirects must stay thin (chat → contact.html only)" >&2
  exit 1
fi

echo "ok: $FILE is thin (chat → contact.html only)"
