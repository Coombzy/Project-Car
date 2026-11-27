#!/usr/bin/env bash
# AUD-021 part 1. Prove the skip path, and that docker, psql, pg_dump, and
# rclone are not invoked. The upgrade path is recorded through ALEMBIC so
# this check does not need a database.
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
target=$ROOT/scripts/test-pg-migrations.sh
api_pwd=$(cd "$ROOT/apps/project-car/api" && pwd)

fail() { printf 'selftest fail: %s\n' "$*" >&2; exit 1; }

[[ -f $target ]] || fail 'AUD-021: missing scripts/test-pg-migrations.sh'
bash -n "$target"
bash -n "$ROOT/scripts/selftest-test-pg-migrations.sh"

if grep -q '/home/box' "$target"; then
  fail 'machine-local path'
fi

if grep -E -q '(^|[^[:alnum:]_])(docker|psql|pg_dump|rclone)([^[:alnum:]_]|$)' "$target"; then
  fail 'migration script names docker, psql, pg_dump, or rclone'
fi

guard=$(mktemp -d)
trap 'rm -rf "$guard"' EXIT
log=$guard/log
calls=$guard/calls
: >"$log"

for cmd in docker psql pg_dump rclone alembic; do
  cat >"$guard/$cmd" <<'EOF'
#!/bin/sh
printf '%s\n' "$0 $*" >> "${CLI_GUARD_LOG:?}"
exit 99
EOF
  chmod +x "$guard/$cmd"
done

recorder=$guard/record-alembic
cat >"$recorder" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "${ALEMBIC_LOG:?}"
printf '%s\n' "DATABASE_URL=${DATABASE_URL-}" >> "${ALEMBIC_LOG:?}"
printf '%s\n' "PWD=$(pwd)" >> "${ALEMBIC_LOG:?}"
exit 0
EOF
chmod +x "$recorder"

invoke() {
  : >"$log"
  set +e
  (
    unset TEST_DATABASE_URL ALEMBIC DATABASE_URL ALEMBIC_LOG
    export CLI_GUARD_LOG="$log" PATH="$guard:/usr/bin:/bin"
    for assignment in "$@"; do
      export "$assignment"
    done
    bash "$target" >"$guard/out" 2>"$guard/err"
  )
  invoke_ec=$?
  set -e
}

assert_no_forbidden() {
  if [[ -s $log ]] && grep -E -q '(^|/)(docker|psql|pg_dump|rclone)([[:space:]]|$)' "$log"; then
    fail "$1 invoked docker, psql, pg_dump, or rclone: $(cat "$log")"
  fi
}

assert_no_cli() {
  assert_no_forbidden "$1"
  if [[ -s $log ]]; then
    fail "$1 invoked a guarded CLI: $(cat "$log")"
  fi
}

invoke DATABASE_URL='postgresql+psycopg://should-not-run@127.0.0.1:1/nope'
[[ $invoke_ec -eq 0 ]] || fail "unset URL: exit $invoke_ec"
[[ $(cat "$guard/out") == 'skip: TEST_DATABASE_URL is unset' ]] || fail "unset URL: stdout=$(cat "$guard/out")"
[[ ! -s $guard/err ]] || fail "unset URL: stderr=$(cat "$guard/err")"
assert_no_cli 'unset URL'

invoke TEST_DATABASE_URL= ALEMBIC="$guard/alembic" \
  DATABASE_URL='postgresql+psycopg://should-not-run@127.0.0.1:1/nope'
[[ $invoke_ec -eq 0 ]] || fail "empty URL: exit $invoke_ec"
[[ $(cat "$guard/out") == 'skip: TEST_DATABASE_URL is unset' ]] || fail "empty URL: stdout=$(cat "$guard/out")"
assert_no_cli 'empty URL'

invoke TEST_DATABASE_URL='sqlite:////tmp/aud021-not-postgres.db' ALEMBIC="$recorder" ALEMBIC_LOG="$calls"
[[ $invoke_ec -ne 0 ]] || fail 'non-postgres URL exited 0'
[[ $(cat "$guard/err") == 'TEST_DATABASE_URL must be a Postgres URL' ]] || fail "non-postgres stderr=$(cat "$guard/err")"
[[ ! -s $calls ]] || fail "non-postgres URL invoked alembic: $(cat "$calls")"
assert_no_cli 'non-postgres URL'

for url in \
  'postgresql+psycopg://projectcar:projectcar@127.0.0.1:1/projectcar_migration_selftest' \
  'postgresql://projectcar:projectcar@127.0.0.1:1/projectcar_migration_selftest' \
  'postgres://projectcar:projectcar@127.0.0.1:1/projectcar_migration_selftest'
do
  : >"$calls"
  invoke TEST_DATABASE_URL="$url" ALEMBIC="$recorder" ALEMBIC_LOG="$calls"
  [[ $invoke_ec -eq 0 ]] || fail "run path exit $invoke_ec stderr=$(cat "$guard/err") stdout=$(cat "$guard/out")"
  [[ $(cat "$guard/out") != *skip:\ TEST_DATABASE_URL\ is\ unset* ]] || fail 'run path took the skip branch'
  assert_no_cli 'run path'
  expected=$guard/expected
  cat >"$expected" <<EOF
upgrade head
DATABASE_URL=${url}
PWD=${api_pwd}
downgrade base
DATABASE_URL=${url}
PWD=${api_pwd}
upgrade head
DATABASE_URL=${url}
PWD=${api_pwd}
check
DATABASE_URL=${url}
PWD=${api_pwd}
EOF
  if ! diff -u "$expected" "$calls" >"$guard/diff"; then
    fail "alembic sequence for ${url%%:*}: $(cat "$guard/diff")"
  fi
done

: >"$calls"
invoke TEST_DATABASE_URL='postgresql+psycopg://projectcar:projectcar@127.0.0.1:1/projectcar_migration_selftest' \
  ALEMBIC="$guard/alembic" ALEMBIC_LOG="$calls"
[[ $invoke_ec -eq 99 ]] || fail "alembic failure: exit $invoke_ec"
assert_no_forbidden 'alembic failure'
[[ -s $log ]] || fail 'alembic failure did not invoke the alembic binary'

printf 'ok\n'
