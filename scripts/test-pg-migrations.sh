#!/usr/bin/env bash
# AUD-021 part 1. When TEST_DATABASE_URL is set, upgrade, downgrade to base,
# upgrade again, then `alembic check` against that Postgres URL. When it is
# unset or empty, skip (exit 0). Alembic reads DATABASE_URL (see
# apps/project-car/api/alembic/env.py). ALEMBIC, when set, is the binary.
set -euo pipefail

if [[ -z ${TEST_DATABASE_URL:-} ]]; then
  printf '%s\n' 'skip: TEST_DATABASE_URL is unset'
  exit 0
fi

case ${TEST_DATABASE_URL} in
  postgres://*|postgresql://*|postgresql+*) ;;
  *)
    printf '%s\n' 'TEST_DATABASE_URL must be a Postgres URL' >&2
    exit 1
    ;;
esac

root=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
api=${root}/apps/project-car/api

if [[ -n ${ALEMBIC:-} ]]; then
  alembic_bin=${ALEMBIC}
elif [[ -x ${api}/.venv/bin/alembic ]]; then
  alembic_bin=${api}/.venv/bin/alembic
else
  alembic_bin=alembic
fi

export DATABASE_URL="${TEST_DATABASE_URL}"
cd "${api}"
"${alembic_bin}" upgrade head
"${alembic_bin}" downgrade base
"${alembic_bin}" upgrade head
"${alembic_bin}" check
