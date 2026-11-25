#!/bin/sh
# Throwaway restore drill. Same-name refusal happens before any client connection.
set -eu

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is required" >&2
  exit 1
fi

source_db=${DATABASE_URL##*/}
source_db=${source_db%%\?*}
target=projectcar_restore_check

if [ "$source_db" = "$target" ]; then
  echo "refusing: source database would be dropped" >&2
  exit 2
fi
if [ -n "${RESTORE_TARGET_DB:-}" ] && [ "$RESTORE_TARGET_DB" = "$source_db" ]; then
  echo "refusing: source database would be dropped" >&2
  exit 2
fi

pathless=${DATABASE_URL%%\?*}
query=
case $DATABASE_URL in
  *\?*) query="?${DATABASE_URL#*\?}" ;;
esac
target_url="${pathless%/*}/${target}${query}"
case $target_url in
  */"$source_db"|*/"$source_db"\?*)
    echo "refusing: source database would be dropped" >&2
    exit 2
    ;;
esac

dump=$(mktemp)
throwaway_created=0
cleanup() {
  status=$?
  rm -f "$dump"
  if [ "$throwaway_created" = 1 ]; then
    psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS projectcar_restore_check" || true
  fi
  exit "$status"
}
trap cleanup EXIT
pg_dump -Fc --dbname="$DATABASE_URL" --file="$dump"
# Literal throwaway name only — the source name is never dropped.
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS projectcar_restore_check"
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c "CREATE DATABASE projectcar_restore_check"
throwaway_created=1
pg_restore --exit-on-error --dbname="$target_url" "$dump"
if [ -n "${RESTORE_DRILL_TAMPER_SQL:-}" ]; then
  psql "$target_url" -v ON_ERROR_STOP=1 -c "$RESTORE_DRILL_TAMPER_SQL"
fi
api_dir=$(CDPATH= cd -- "$(dirname "$0")/../apps/project-car/api" && pwd)
( cd "$api_dir" && DATABASE_URL="$target_url" alembic current )
mismatch=0
for table in members bookings token_transactions billing_transactions; do
  src=$(psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -Atqc "SELECT count(*) FROM $table")
  dst=$(psql "$target_url" -v ON_ERROR_STOP=1 -Atqc "SELECT count(*) FROM $table")
  printf '%s source=%s throwaway=%s\n' "$table" "$src" "$dst"
  [ "$src" = "$dst" ] || mismatch=1
done
[ "$mismatch" = 0 ] || exit 1
ledger="$api_dir/scripts/reconcile_ledger.py"
if [ -f "$ledger" ]; then
  ( cd "$api_dir" && DATABASE_URL="$target_url" python3 "$ledger" )
else
  echo "skip reconcile_ledger.py: file absent"
fi
