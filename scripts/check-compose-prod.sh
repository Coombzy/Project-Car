#!/usr/bin/env bash
# Postgres must stay on 127.0.0.1, and prod must refuse a default password.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
dev="$root/infra/compose/compose.yaml"
prod="$root/infra/compose/compose.prod.yaml"
proj=$(mktemp -d)
trap 'rm -rf "$proj"' EXIT

die() { printf '%s\n' "$*" >&2; exit 1; }

render() {
  local file="$1"
  shift
  # Options such as -u must come before name=value, or env treats -u as the command.
  env "$@" COMPOSE_DISABLE_ENV_FILE=1 \
    docker compose --project-directory "$proj" -f "$file" config
}

check_ports() {
  printf '%s\n' "$1" | awk '
    function flush() {
      if (!in_port) return
      if (host == "") {
        printf "postgres %s port has no host IP\n", svc > "/dev/stderr"
        bad = 1
      } else if (host != "127.0.0.1") {
        printf "postgres %s port host %s\n", svc, host > "/dev/stderr"
        bad = 1
      }
      in_port = 0
      host = ""
    }
    /^[^ ]/ { section = $1; next }
    section != "services:" { next }
    /^  [^ ]/ {
      flush()
      svc = $1
      sub(/:$/, "", svc)
      pg = (svc ~ /postgres/)
      in_ports = 0
      next
    }
    /^    image:/ && /postgres/ { pg = 1 }
    pg && /^    ports:/ { in_ports = 1; next }
    pg && in_ports && /^    [^ ]/ { flush(); in_ports = 0 }
    pg && in_ports && /^      - / {
      flush()
      in_port = 1
      line = $0
      sub(/^      - /, "", line)
      gsub(/["\047]/, "", line)
      if (line ~ /^host_ip:/) {
        sub(/^host_ip: */, "", line)
        host = line
      } else if (line ~ /^([0-9]+\.){3}[0-9]+:[0-9]+:[0-9]+$/) {
        split(line, a, ":")
        host = a[1]
      }
      next
    }
    pg && in_port && /^        host_ip:/ {
      host = $2
      gsub(/["\047]/, "", host)
      next
    }
    END { flush(); exit bad }
  '
}

cfg=$(render "$dev" SHOP_POSTGRES_PASSWORD=stand-in-pw)
check_ports "$cfg" || die "loopback check failed: compose.yaml"
cfg=$(render "$prod" SHOP_POSTGRES_PASSWORD=stand-in-pw)
check_ports "$cfg" || die "loopback check failed: compose.prod.yaml"

set +e
out=$(render "$dev" -u SHOP_POSTGRES_PASSWORD 2>&1)
rc=$?
set -e
if [[ $rc -eq 0 ]]; then
  if printf '%s\n' "$out" | grep -Eq '^[[:space:]]*POSTGRES_PASSWORD:[[:space:]]*"?projectcar"?[[:space:]]*$'; then
    die "compose.yaml rendered POSTGRES_PASSWORD=projectcar"
  fi
elif ! printf '%s\n' "$out" | grep -q 'SHOP_POSTGRES_PASSWORD'; then
  die "compose.yaml did not refuse an unset SHOP_POSTGRES_PASSWORD"
fi

set +e
out=$(render "$prod" -u SHOP_POSTGRES_PASSWORD 2>&1)
rc=$?
set -e
if [[ $rc -eq 0 ]]; then
  die "compose.prod.yaml rendered without SHOP_POSTGRES_PASSWORD"
fi
if ! printf '%s\n' "$out" | grep -Eq 'required variable SHOP_POSTGRES_PASSWORD|Set SHOP_POSTGRES_PASSWORD'; then
  die "compose.prod.yaml missing :? refusal for SHOP_POSTGRES_PASSWORD"
fi
