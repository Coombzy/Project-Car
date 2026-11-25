#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash -n scripts/audit-deps.sh
bash -n scripts/selftest-audit-deps.sh
grep -q -F "npm audit --omit=dev --audit-level=high" scripts/audit-deps.sh
if grep -q '/home/box' scripts/audit-deps.sh; then
  echo "audit-deps.sh contains a machine-local path" >&2
  exit 1
fi

found=0
while IFS= read -r line || [[ -n "$line" ]]; do
  code="${line%%#*}"
  [[ "$code" == *pip-audit* ]] || continue
  found=1
  if [[ "$code" =~ (^|[[:space:]])(-r|--requirement)[[:space:]]+[^[:space:]]*pyproject\.toml ]]; then
    echo "pip-audit -r does not take pyproject.toml" >&2
    exit 1
  fi
  if [[ ! "$code" =~ pip-audit[[:space:]]+.*(-r[[:space:]]|--requirement[[:space:]]|apps/project-car/api) ]]; then
    echo "pip-audit needs a requirements file or the API project directory" >&2
    exit 1
  fi
done < scripts/audit-deps.sh
if [[ "$found" -eq 0 ]]; then
  echo "pip-audit invocation missing" >&2
  exit 1
fi
echo ok
