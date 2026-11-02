#!/usr/bin/env bash
# selftest-related-tests.sh: checks scripts/related-tests.py maps files without running anything.
set -euo pipefail
cd "$(dirname "$0")/.."
out=$(python3 scripts/related-tests.py README.md); grep -q "nothing to run" <<<"$out" || { echo "FAIL docs-only: $out"; exit 1; }
if [[ -d apps/project-car ]]; then
  t=$(ls apps/project-car/api/tests/test_*.py | head -1)
  out=$(python3 scripts/related-tests.py "$t"); grep -q "pytest.*$(basename "$t")" <<<"$out" || { echo "FAIL api test: $out"; exit 1; }
  out=$(python3 scripts/related-tests.py apps/project-car/web/lib/shop-api.ts); grep -q "npm run -s typecheck" <<<"$out" || { echo "FAIL web: $out"; exit 1; }
else
  out=$(python3 scripts/related-tests.py scripts/v0-proof.ts); grep -q "v0-proof" <<<"$out" || { echo "FAIL pbay proof: $out"; exit 1; }
fi
grep -q /home/box scripts/related-tests.py && { echo "FAIL: box path in script"; exit 1; }
echo "selftest ok"
