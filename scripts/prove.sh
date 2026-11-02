#!/usr/bin/env bash
# Record red, then green, for a pull request body.
# Usage: scripts/prove.sh red|green
# PROVE_CMD, when set, replaces the repo suite (shell command, repo root).
set -euo pipefail

ROOT=$(unset CDPATH; cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
PROOF="$ROOT/.agent-proof/proof.json"

usage() { printf 'Usage: scripts/prove.sh red|green\n' >&2; }

if [[ $# -ne 1 ]]; then usage; exit 2; fi
phase=$1
case "$phase" in
  red|green) ;;
  -h|--help) usage; exit 0 ;;
  *) usage; exit 2 ;;
esac

sha=$(git rev-parse HEAD) || { printf 'prove FAIL: not a git checkout\n' >&2; exit 2; }
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)

run_default() {
  ( cd "$ROOT/apps/project-car/api" && pytest -q ) || return $?
  ( cd "$ROOT/apps/project-car/web" && npm run lint && npm test ) || return $?
}

ec=0
if [[ -n "${PROVE_CMD:-}" ]]; then
  cmd=$(printf 'set -euo pipefail; cd %q && %s' "$ROOT" "$PROVE_CMD")
  bash -c "$cmd" || ec=$?
else
  run_default || ec=$?
fi

# Last red and last green, one JSON object. Missing phase is null.
phase_value() {
  local which=$1
  if [[ ! -f "$PROOF" ]]; then
    printf 'null'
    return 0
  fi
  awk -v p="$which" '
    $0 ~ "^  \"" p "\":" {
      sub(/^  "[a-z]+": /, "")
      sub(/,$/, "")
      print
      found = 1
      exit
    }
    END { if (!found) printf "null" }
  ' "$PROOF"
}

mkdir -p "$ROOT/.agent-proof"
red_json=$(phase_value red)
green_json=$(phase_value green)
current=$(printf '{"phase": "%s", "sha": "%s", "exit_code": %s, "time": "%s"}' "$phase" "$sha" "$ec" "$now")
if [[ "$phase" == red ]]; then red_json=$current; else green_json=$current; fi
cat > "$PROOF" <<EOF
{
  "red": ${red_json},
  "green": ${green_json}
}
EOF

if [[ "$phase" == red ]]; then
  if [[ "$ec" -ne 0 ]]; then
    printf 'prove: red failed as expected sha=%s exit_code=%s\n' "$sha" "$ec"
    exit 0
  fi
  printf 'prove FAIL: red suite unexpectedly passed sha=%s\n' "$sha" >&2
  exit 1
fi

if [[ "$ec" -ne 0 ]]; then
  printf 'prove FAIL: green suite failed exit_code=%s\n' "$ec" >&2
  exit 2
fi

red_line=$(phase_value red)
red_sha=$(printf '%s\n' "$red_line" | sed -n 's/.*"sha": "\([0-9a-f][0-9a-f]*\)".*/\1/p')
red_ec=$(printf '%s\n' "$red_line" | sed -n 's/.*"exit_code": \([0-9][0-9]*\).*/\1/p')
if [[ -z "$red_sha" || -z "$red_ec" || "$red_ec" == 0 || "$red_sha" == "$sha" ]]; then
  printf 'prove FAIL: need a recorded red with nonzero exit on a different sha (red=%s exit_code=%s head=%s)\n' \
    "${red_sha:-none}" "${red_ec:-none}" "$sha" >&2
  exit 2
fi
printf 'RED commit: %s\nGREEN commit: %s\n' "$red_sha" "$sha"
exit 0
