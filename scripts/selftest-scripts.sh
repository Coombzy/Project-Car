#!/usr/bin/env bash
# run the named selftests from repo root; print ok when all exit 0
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

for s in \
  scripts/selftest-check-result.sh \
  scripts/selftest-pr-ready.sh \
  scripts/selftest-related-tests.sh \
  scripts/selftest-agent-scripts.sh \
  scripts/selftest-check-compose-prod.sh
do
  if ! bash "$s"; then
    printf 'failed: %s\n' "$s" >&2
    exit 1
  fi
done

printf 'ok\n'
