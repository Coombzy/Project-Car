#!/usr/bin/env bash
# RED: proof-shots-selftest expects the --self-test hook to print ok.
set -euo pipefail
ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
out=$(bash "$ROOT/scripts/proof-shots.sh" --self-test)
[[ "$out" == "ok" ]] || {
  printf 'selftest fail: out=%s\n' "$out" >&2
  exit 1
}
printf 'ok\n'
