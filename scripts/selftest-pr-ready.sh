#!/usr/bin/env bash
# RED: expects READY on main; pr-ready.sh should refuse on_main.
set -euo pipefail
ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
git -C "$TMP" init -q -b main
git -C "$TMP" config user.email "t@example.com"
git -C "$TMP" config user.name "t"
git -C "$TMP" config commit.gpgsign false
mkdir -p "$TMP/scripts" "$TMP/tests"
cp "$ROOT/scripts/pr-ready.sh" "$TMP/scripts/pr-ready.sh"
printf 'def test_foo():\n    pass\n' > "$TMP/tests/test_foo.py"
git -C "$TMP" add scripts/pr-ready.sh tests/test_foo.py
git -C "$TMP" commit -q -m init
git -C "$TMP" update-ref refs/remotes/origin/main HEAD
out=$(cd "$TMP" && bash scripts/pr-ready.sh --no-tests 2>/dev/null) || true
[[ "$out" == READY ]] || { printf 'selftest fail: got %s want READY\n' "$out" >&2; exit 1; }
printf 'ok\n'
