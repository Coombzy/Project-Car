#!/usr/bin/env bash
# Feed fixture compose-config text to check_ports. Never call docker.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
target="$root/scripts/check-compose-prod.sh"
dev="$root/infra/compose/compose.yaml"
prod="$root/infra/compose/compose.prod.yaml"

fail() { printf '%s\n' "$*" >&2; exit 1; }

hook_line=$(grep -m 1 -n -- '--self-test' "$target" | cut -d: -f1 || true)
call_line=$(grep -m 1 -n 'cfg=$(render' "$target" | cut -d: -f1 || true)
if [[ -z "${hook_line}" || -z "${call_line}" || "${hook_line}" -ge "${call_line}" ]]; then
  fail "missing --self-test hook before render"
fi

guard=$(mktemp -d)
trap 'rm -rf "$guard"' EXIT
printf '%s\n' '#!/bin/sh' 'printf "%s\n" "docker invoked: $*" >> "${DOCKER_GUARD_LOG:?}"' 'exit 99' > "$guard/docker"
chmod +x "$guard/docker"
export DOCKER_GUARD_LOG="$guard/log"
: > "$DOCKER_GUARD_LOG"
export PATH="$guard:$PATH"

run() {
  local expect=$1 label=$2 fixture=$3 rc err
  err="$guard/err"
  set +e
  printf '%s\n' "$fixture" | bash "$target" --self-test >/dev/null 2>"$err"
  rc=$?
  set -e
  if [[ $expect == pass && $rc -ne 0 ]]; then
    fail "$label: expected pass, rc=$rc, err=$(cat "$err")"
  fi
  if [[ $expect == fail && $rc -eq 0 ]]; then
    fail "$label: expected fail"
  fi
}

short() {
  cat << EOF
name: project-car-shop
services:
  shop-postgres:
    image: postgres:16
    ports:
      - "$1"
EOF
}

long() {
  cat << EOF
name: project-car-shop
services:
  shop-postgres:
    image: postgres:16
    ports:
      - mode: ingress
        host_ip: $1
        target: 5432
        published: "5432"
        protocol: tcp
EOF
}

none() {
  cat << 'YAML'
name: project-car-shop
services:
  shop-postgres:
    image: postgres:16
    ports:
      - mode: ingress
        target: 5432
        published: "5432"
        protocol: tcp
YAML
}

run pass "loopback-short" "$(short '127.0.0.1:5432:5432')"
run fail "open-short" "$(short '0.0.0.0:5432:5432')"
run fail "no-host-short" "$(short '5432:5432')"
run pass "loopback-long" "$(long '127.0.0.1')"
run fail "open-long" "$(long '0.0.0.0')"
run fail "no-host-long" "$(none)"

if [[ -s "$DOCKER_GUARD_LOG" ]]; then
  fail "docker was invoked: $(cat "$DOCKER_GUARD_LOG")"
fi

grep -q 'SHOP_POSTGRES_PASSWORD:?' "$dev" || fail "dev compose missing password refusal"
grep -q 'SHOP_POSTGRES_PASSWORD:?' "$prod" || fail "prod compose missing password refusal"
if grep -q 'SHOP_POSTGRES_PASSWORD:-' "$dev" "$prod"; then
  fail "postgres password has a default"
fi
grep -q 'POSTGRES_PASSWORD=projectcar' "$target" || fail "checker missing default password refusal"
grep -Eq 'required variable SHOP_POSTGRES_PASSWORD|Set SHOP_POSTGRES_PASSWORD' "$target" || fail "checker missing prod password refusal"

printf '%s\n' ok
