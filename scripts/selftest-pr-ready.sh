#!/usr/bin/env bash
# Selftest for scripts/pr-ready.sh. Throwaway git repo; no Shop OS pytest/npm.
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

git -C "$TMP" init -q -b main
git -C "$TMP" config user.email "t@example.com"
git -C "$TMP" config user.name "t"
git -C "$TMP" config commit.gpgsign false

mkdir -p "$TMP/scripts" "$TMP/tests"
cp "$ROOT/scripts/pr-ready.sh" "$TMP/scripts/pr-ready.sh"
printf 'def test_foo():\n    pass\n' > "$TMP/tests/test_foo.py"
git -C "$TMP" add scripts/pr-ready.sh tests/test_foo.py
git -C "$TMP" commit -q -m init
git -C "$TMP" update-ref refs/remotes/origin/main HEAD

fail() { printf 'selftest fail: %s\n' "$*" >&2; exit 1; }

expect() {
  local want_ec=$1 want=$2
  shift 2
  local out ec
  set +e
  out=$(cd "$TMP" && bash scripts/pr-ready.sh "$@" 2>/dev/null)
  ec=$?
  set -e
  [[ "$ec" -eq "$want_ec" && "$out" == "$want" ]] || fail "got ec=$ec out=$out want=$want_ec $want"
}

branch() {
  git -C "$TMP" checkout -q main
  git -C "$TMP" reset -q --hard
  git -C "$TMP" clean -fdq
  git -C "$TMP" checkout -q -b "$1"
}

expect 1 'NOT_READY|on_main' --no-tests

branch dirty-br
printf 'x\n' > "$TMP/dirty.txt"
expect 1 'NOT_READY|dirty' --no-tests

branch wf-br
mkdir -p "$TMP/.github/workflows"
printf 'name: t\n' > "$TMP/.github/workflows/ci.yml"
git -C "$TMP" add .github/workflows/ci.yml
git -C "$TMP" commit -q -m wf
expect 1 'NOT_READY|workflows' --no-tests

branch del-br
git -C "$TMP" rm -q tests/test_foo.py
git -C "$TMP" commit -q -m del
expect 1 'NOT_READY|deleted_test' --no-tests

branch skip-br
printf 'pytest.mark.skip\n' > "$TMP/tests/test_skip.py"
git -C "$TMP" add tests/test_skip.py
git -C "$TMP" commit -q -m skip
expect 1 'NOT_READY|skip_marker' --no-tests

branch sec-br
printf 'not-a-real-key\n' > "$TMP/id_rsa"
git -C "$TMP" add id_rsa
git -C "$TMP" commit -q -m sec
expect 1 'NOT_READY|secret_file' --no-tests

branch ok-br
printf 'def answer():\n    return 1\n' > "$TMP/pkg.py"
printf 'def test_pkg():\n    assert True\n' > "$TMP/tests/test_pkg.py"
git -C "$TMP" add pkg.py tests/test_pkg.py
git -C "$TMP" commit -q -m ok
expect 0 READY --no-tests

printf 'ok\n'
