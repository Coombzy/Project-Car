#!/usr/bin/env bash
# Local preflight. Prints READY or NOT_READY|reason. Exit 0 only when READY.
# Usage: scripts/pr-ready.sh [base] [--no-tests]
# base defaults to origin/main. PROVE_CMD overrides the proof suite.
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

BASE="origin/main"
RUN_TESTS=1
for arg in "$@"; do
  case "$arg" in
    --no-tests) RUN_TESTS=0 ;;
    -h|--help)
      printf 'Usage: scripts/pr-ready.sh [base] [--no-tests]\n' >&2
      exit 0
      ;;
    *) BASE=$arg ;;
  esac
done

not_ready() { printf 'NOT_READY|%s\n' "$1"; exit 1; }

git fetch origin main >/dev/null 2>&1 || true

br=$(git rev-parse --abbrev-ref HEAD)
case "$br" in
  main|master) not_ready "on_${br}" ;;
esac

git rev-parse -q --verify "${BASE}^{commit}" >/dev/null 2>&1 || not_ready "missing_base"
mb=$(git merge-base HEAD "$BASE") || not_ready "no_merge_base"

names=$(git diff --name-only --no-renames "$mb" HEAD)
wf=$(printf '%s\n' "$names" | grep -E '^\.github/workflows/' || true)
[[ -z "$wf" ]] || not_ready "workflows"

TEST_RE='(^|/)(tests?|__tests__|e2e)/|(^|/)test_[^/]*\.py$|_test\.(py|go)$|\.(test|spec)\.[jt]sx?$'
status=$(git diff --name-status --no-renames "$mb" HEAD)
del=$(printf '%s\n' "$status" | awk '$1=="D"{print $2}' | grep -E "$TEST_RE" || true)
[[ -z "$del" ]] || not_ready "deleted_test"

difftext=$(git diff -U0 --no-renames "$mb" HEAD)
SKIP_RE='pytest\.mark\.(skip|xfail)|pytest\.(skip|xfail)\(|@unittest\.(skip|expectedFailure)|\b(it|test|describe)\.(skip|only|fixme)\(|\b(xit|xdescribe|fit|fdescribe)\(|test\.fail\('
skip=$(printf '%s\n' "$difftext" | grep -E '^\+' | grep -vE '^\+\+\+' | grep -E "$SKIP_RE" || true)
[[ -z "$skip" ]] || not_ready "skip_marker"

SECRET_RE='(^|/)\.env($|\.)|(^|/)[^/]*\.(pem|p12|pfx)$|(^|/)(id_rsa|id_dsa|id_ed25519)(\.pub)?$|(^|/)[^/]*\.key$|(^|/)(credentials|secrets)\.(json|ya?ml|txt|env)$'
added=$(git diff --name-only --diff-filter=A --no-renames "$mb" HEAD)
sec=$(printf '%s\n' "$added" | grep -E "$SECRET_RE" | grep -vE '(^|/)\.env\.(example|sample|template)$' || true)
[[ -z "$sec" ]] || not_ready "secret_file"

SIZE_RE='(^|/)(package-lock\.json|npm-shrinkwrap\.json|pnpm-lock\.yaml|yarn\.lock|poetry\.lock|uv\.lock|Cargo\.lock|Gemfile\.lock|[^/]*\.lock)$|(^|/)__snapshots__/|\.snap$|-snapshots/|(^|/)(baselines?|snapshots|generated|dist|build)/|\.min\.(js|css)$|\.(png|jpe?g|gif|webp|svg)$|(^|/)proof/'
numstat=$(git diff --numstat --no-renames "$mb" HEAD)
n=$(printf '%s\n' "$numstat" | SIZE_RE="$SIZE_RE" awk -F '\t' 'BEGIN { re = ENVIRON["SIZE_RE"] } $1 != "-" && $3 !~ re { s += $1 + $2 } END { print s + 0 }')
if (( n > 600 )); then not_ready "changed_lines=${n}"; fi
if (( n > 300 )); then printf 'WARN|changed_lines=%s\n' "$n" >&2; fi

dirty=$(git status --porcelain)
[[ -z "$dirty" ]] || not_ready "dirty"

run_default() {
  ( cd "$ROOT/apps/project-car/api" && pytest -q ) || return $?
  ( cd "$ROOT/apps/project-car/web" && npm run lint && npm test ) || return $?
}

if [[ "$RUN_TESTS" -eq 1 ]]; then
  ec=0
  if [[ -n "${PROVE_CMD:-}" ]]; then
    cmd=$(printf 'set -euo pipefail; cd %q && %s' "$ROOT" "$PROVE_CMD")
    bash -c "$cmd" || ec=$?
  else
    run_default || ec=$?
  fi
  [[ "$ec" -eq 0 ]] || not_ready "tests"
fi

printf 'READY\n'
exit 0
