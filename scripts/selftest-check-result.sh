#!/usr/bin/env bash
# Selftest for scripts/check-result.sh. Throwaway queue; does not merge.
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/scripts" "$TMP/Docs"
cp "$ROOT/scripts/check-result.sh" "$ROOT/scripts/next-row.sh" "$TMP/scripts/"

fail() { printf 'selftest fail: %s\n' "$*" >&2; exit 1; }

expect() {
  local want_ec=$1 want_out=$2 want_err=$3
  shift 3
  local out err ec
  set +e
  out=$(cd "$TMP" && sh scripts/check-result.sh "$@" 2>"$TMP/err")
  ec=$?
  set -e
  err=$(cat "$TMP/err")
  [[ "$ec" -eq "$want_ec" && "$out" == "$want_out" && "$err" == "$want_err" ]] \
    || fail "ec=$ec out=$out err=$err"
}

expect 2 '' 'conclusion must be success or failure' maybe 9 br
expect 2 '' 'pr and branch are required' success 9
expect 0 '| Queue check failed on PR 9 br; leave the pull request open | proof | |' '' failure 9 br

printf '## Now\n\nOpen the bay.\n\n## Already on main\n\nkept\n' > "$TMP/Docs/queue.md"
expect 0 $'merge pull request 9 br\nmove to Already on main: Open the bay.' '' success 9 br

printf '## Now\n\nNo open row\n' > "$TMP/Docs/queue.md"
expect 2 '' 'no open row to move' success 9 br

printf 'ok\n'
