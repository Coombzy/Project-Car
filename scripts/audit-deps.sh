#!/usr/bin/env bash
# Production dependency audits for the Shop OS web app and API.
# Exits non-zero if npm audit or pip-audit is missing or fails.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
status=0

( cd apps/project-car/web && npm audit --omit=dev --audit-level=high ) || status=$?
( cd apps/project-car/api && pip-audit ) || status=$?

exit "${status}"
