#!/usr/bin/env bash
# Shop OS dependency install for Cursor cloud agents.
# Mirrors .github/workflows/shop-os-ci.yml install steps only.
# CURSOR_INSTALL_DRY_RUN=1 prints commands and install dirs, then exits.
# CURSOR_INSTALL_BROWSERS=1 also installs Playwright Chromium.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY="${CURSOR_INSTALL_DRY_RUN:-0}"
BROWSERS="${CURSOR_INSTALL_BROWSERS:-0}"

run_in() {
  local dir="$1"
  shift
  echo "install dir: ${dir}"
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  if [[ "${DRY}" == "1" ]]; then
    return 0
  fi
  (cd "${ROOT}/${dir}" && "$@")
}

echo "Cursor install: Shop OS CI dependencies"
run_in apps/project-car/api python -m pip install -e ".[dev]"

if [[ "${BROWSERS}" == "1" ]]; then
  run_in apps/project-car/web npm ci
  run_in apps/project-car/web npx playwright install --with-deps chromium
else
  # npm ci must not download browsers unless explicitly requested.
  run_in apps/project-car/web env PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
fi

echo "Cursor install done."
echo "  api: apps/project-car/api (python -m pip install -e \".[dev]\")"
echo "  web: apps/project-car/web (npm ci)"
if [[ "${BROWSERS}" == "1" ]]; then
  echo "  browsers: chromium (npx playwright install --with-deps chromium)"
else
  echo "  browsers: skipped (set CURSOR_INSTALL_BROWSERS=1 to install Chromium)"
fi
