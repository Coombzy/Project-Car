#!/usr/bin/env bash
# Validate Cursor cloud-agent environment wiring. No package installs.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

python3 -m json.tool .cursor/environment.json >/dev/null

install="$(python3 -c 'import json; print(json.load(open(".cursor/environment.json"))["install"])')"
found=""
for token in ${install}; do
  if [[ -f "${token}" ]]; then
    found="${token}"
  fi
done
if [[ -z "${found}" ]]; then
  echo "install does not reference an existing script: ${install}" >&2
  exit 1
fi

bash -n scripts/cursor-install.sh

if grep -q '/home/box' scripts/cursor-install.sh; then
  echo "cursor-install.sh contains a machine-local path" >&2
  exit 1
fi

out="$(CURSOR_INSTALL_DRY_RUN=1 bash scripts/cursor-install.sh)"
printf '%s\n' "${out}"

for dir in apps/project-car/api apps/project-car/web; do
  if ! printf '%s\n' "${out}" | grep -F "${dir}" >/dev/null; then
    echo "dry run did not print install dir: ${dir}" >&2
    exit 1
  fi
done

echo "selftest ok"
