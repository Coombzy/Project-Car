#!/usr/bin/env bash
# Selftest for scripts/proof-shots.sh. Runs --self-test only; no browser, no golden recapture.
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
out=$(bash "$ROOT/scripts/proof-shots.sh" --self-test)
[[ "$out" == "proof-shots selftest ok" ]] || {
  printf 'selftest fail: out=%s\n' "$out" >&2
  exit 1
}
printf 'ok\n'
