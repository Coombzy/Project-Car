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
  echo "refusing: source database would not be dropped" >&2
  exit 2
fi
if [ -n "${RESTORE_TARGET_DB:-}" ] && [ "$RESTORE_TARGET_DB" = "$source_db" ]; then
  echo "refusing: source database would not be dropped" >&2
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
    echo "refusing: source database would not be dropped" >&2
    exit 2
    ;;
esac

dump=$(mktemp)
trap 'rm -f "$dump"' EXIT
pg_dump -Fc --dbname="$DATABASE_URL" --file="$dump"
# Literal throwaway name only — the source name is never dropped.
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS projectcar_restore_check"
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c "CREATE DATABASE projectcar_restore_check"
pg_restore --exit-on-error --dbname="$target_url" "$dump"
