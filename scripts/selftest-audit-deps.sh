#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash -n scripts/audit-deps.sh
bash -n scripts/selftest-audit-deps.sh
grep -F "npm audit --omit=dev --audit-level=high" scripts/audit-deps.sh
grep -E 'pip-audit.*pyproject.toml|pip-audit -r' scripts/audit-deps.sh
if grep -q '/home/box' scripts/audit-deps.sh; then
  echo "audit-deps.sh contains a machine-local path" >&2
  exit 1
fi
echo ok
