#!/usr/bin/env bash
# RED: check-result-selftest expects a merge when Now has no open row.
set -euo pipefail
ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/scripts" "$TMP/Docs"
cp "$ROOT/scripts/check-result.sh" "$ROOT/scripts/next-row.sh" "$TMP/scripts/"
printf '## Now\n\nNo open row\n' > "$TMP/Docs/queue.md"
set +e
out=$(cd "$TMP" && sh scripts/check-result.sh success 9 br 2>/dev/null)
ec=$?
set -e
[[ "$ec" -eq 0 && "$out" == "merge pull request 9 br" ]] || {
  printf 'selftest fail: ec=%s out=%s\n' "$ec" "$out" >&2
  exit 1
}
printf 'ok\n'
