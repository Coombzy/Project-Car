#!/usr/bin/env bash
# Production dependency audits for the Shop OS web app and API.
# Exits non-zero if npm audit or pip-audit is missing or fails.
# `pip-audit <project dir>` reads [project].dependencies from that
# directory's pyproject.toml (not the ambient environment, not optional extras).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
status=0

( cd apps/project-car/web && npm audit --omit=dev --audit-level=high ) || status=$?
pip-audit "${ROOT}/apps/project-car/api" || status=$?

exit "${status}"
