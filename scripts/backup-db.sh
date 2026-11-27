#!/bin/sh
# Shop dump from DATABASE_URL only. Skip off-site copy when BACKUP_REMOTE is unset.
set -eu

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is required" >&2
  exit 1
fi

backup_dir=${BACKUP_DIR:-/var/backups/project-car}
stamp=$(date -u +%Y%m%dT%H%M%SZ)
dest="${backup_dir}/projectcar-${stamp}.dump"
mkdir -p "$backup_dir"
pg_dump -Fc --dbname="$DATABASE_URL" --file="$dest"

if [ -z "${BACKUP_REMOTE:-}" ]; then
  echo "skip off-site rclone copy: BACKUP_REMOTE is unset"
  exit 0
fi

rclone copy "$dest" "$BACKUP_REMOTE"
