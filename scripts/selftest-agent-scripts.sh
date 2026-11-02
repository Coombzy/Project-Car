#!/usr/bin/env bash
# Throwaway checks for prove.sh and pr-ready.sh. Uses PROVE_CMD, not the real suite.
set -euo pipefail

HERE=$(unset CDPATH; cd -- "$(dirname -- "$0")" && pwd)
fail=0
say() { printf '%s\n' "$*"; }

check() {
  local want_rc=$1 want_re=$2
  shift 2
  local out rc
  set +e
  out=$("$@" 2>&1)
  rc=$?
  set -e
  if [[ "$rc" -eq "$want_rc" ]] && printf '%s\n' "$out" | grep -Eq "$want_re"; then
    say "PASS rc=${want_rc} ${want_re}"
  else
    say "FAIL want rc=${want_rc} re=${want_re} got rc=${rc}"
    printf '%s\n' "$out"
    fail=1
  fi
}

at() { ( cd "$repo" && "$@" ); }

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
repo=$tmp/repo
git init -q -b main "$repo"
git -C "$repo" config user.email t@example.com
git -C "$repo" config user.name t
git -C "$repo" config commit.gpgsign false
mkdir -p "$repo/scripts" "$repo/tests"
cp "$HERE/prove.sh" "$HERE/pr-ready.sh" "$repo/scripts/"
chmod +x "$repo/scripts/prove.sh" "$repo/scripts/pr-ready.sh"
printf 'def test_ok():\n    assert True\n' > "$repo/tests/test_ok.py"
echo init > "$repo/README"
git -C "$repo" add scripts tests README
git -C "$repo" commit -qm init
git -C "$repo" update-ref refs/remotes/origin/main HEAD

commit_file() {
  git -C "$repo" add -- "$1"
  git -C "$repo" commit -qm "update $1"
}

say "selftest $HERE"
git -C "$repo" checkout -q -b prove-a
echo a > "$repo/a.txt"
commit_file a.txt
check 2 'prove FAIL' at env PROVE_CMD=true scripts/prove.sh green
check 0 'red failed as expected' at env PROVE_CMD=false scripts/prove.sh red
echo b > "$repo/b.txt"
commit_file b.txt
check 0 'RED commit:' at env PROVE_CMD=true scripts/prove.sh green
check 0 'GREEN commit:' at env PROVE_CMD=true scripts/prove.sh green

rm -rf "$repo/.agent-proof"
git -C "$repo" checkout -q -B wf origin/main
mkdir -p "$repo/.github/workflows"
echo x > "$repo/.github/workflows/ci.yml"
commit_file .github/workflows/ci.yml
check 1 'NOT_READY\|workflows' at scripts/pr-ready.sh

git -C "$repo" checkout -q -B del origin/main
git -C "$repo" rm -q tests/test_ok.py
git -C "$repo" commit -qm 'delete test'
check 1 'NOT_READY\|deleted_test' at scripts/pr-ready.sh

git -C "$repo" checkout -q -B skipm origin/main
printf '\npytest.%s("nope")\n' skip >> "$repo/tests/test_ok.py"
commit_file tests/test_ok.py
check 1 'NOT_READY\|skip_marker' at scripts/pr-ready.sh

git -C "$repo" checkout -q -B ok origin/main
echo hello >> "$repo/README"
commit_file README
check 0 '^READY$' at env PROVE_CMD=true scripts/pr-ready.sh origin/main

if [[ "$fail" -ne 0 ]]; then
  say "SELFTEST FAIL"
  exit 1
fi
say "ALL PASS"
