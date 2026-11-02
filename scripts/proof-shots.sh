#!/usr/bin/env bash
# proof-shots.sh: before/after screenshots of named pages at 390 and 1440 for a PR's Proof section.
#   bash scripts/proof-shots.sh <page>...      page = visual test name, e.g. schedule member-home
#   bash scripts/proof-shots.sh --list         page names
#   bash scripts/proof-shots.sh --self-test    argument and table checks, no browser
# Before = the committed reference image on origin/main (main's look). After = this tree, rendered fresh by the
# visual suite (apps/project-car/web/visual, seeded api + next start). Writes .proof-shots/<page>-<before|after>-<w>.png
# and .proof-shots/shots.md (paste into the PR; host the images, do not commit .proof-shots/). Your committed reference images
# are left exactly as they were. Needs: scripts/cursor-install.sh with CURSOR_INSTALL_BROWSERS=1, and `npm run build`
# in apps/project-car/web (done here unless PROOF_SHOTS_SKIP_BUILD=1).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; WEB="$ROOT/apps/project-car/web"; SHOTS="$WEB/visual/screenshots"
OUT="${PROOF_SHOTS_OUT:-$ROOT/.proof-shots}"; WIDTHS=(390 1440)
die(){ echo "proof-shots: $*" >&2; exit 2; }
pages(){ grep -oE '(name: "|test\(")[a-z0-9-]+"' "$WEB/visual/pages.spec.ts" | sed -E 's/.*"([a-z0-9-]+)"/\1/' | sort -u; }
table(){  # table <out> <page>...
  local o="$1" p w; shift
  { echo "| Page | Width | Before (main) | After |"; echo "|---|---|---|---|"
    for p in "$@"; do for w in "${WIDTHS[@]}"; do
      echo "| $p | $w | ![]($p-before-$w.png) | ![]($p-after-$w.png) |"; done; done; } > "$o/shots.md"
}
self_test(){
  local t; t="$(mktemp -d)"; trap 'rm -rf "$t"' RETURN
  pages | grep -qx schedule || { echo "FAIL: page list lacks schedule"; return 1; }
  ( PROOF_SHOTS_OUT="$t" bash "$0" no-such-page >/dev/null 2>&1 ) && { echo "FAIL: unknown page accepted"; return 1; }
  ( bash "$0" >/dev/null 2>&1 ) && { echo "FAIL: no page accepted"; return 1; }
  table "$t" schedule; [[ $(grep -c '^| schedule' "$t/shots.md") == 2 ]] || { echo "FAIL: table"; return 1; }
  grep -q "/home/""box" "$0" && { echo "FAIL: box path"; return 1; }
  echo "proof-shots selftest ok"
}
case "${1:-}" in --self-test) self_test; exit;; --list) pages; exit 0;; "") die "usage: proof-shots.sh <page>... (see --list)";; esac
known="$(pages)"; for p in "$@"; do grep -qx "$p" <<<"$known" || die "unknown page '$p' (see --list)"; done
mkdir -p "$OUT"; base=origin/main; git -C "$ROOT" rev-parse -q --verify "$base" >/dev/null || base=main
for p in "$@"; do for w in "${WIDTHS[@]}"; do
  git -C "$ROOT" show "$base:apps/project-car/web/visual/screenshots/$w/$p.png" > "$OUT/$p-before-$w.png" 2>/dev/null \
    || { rm -f "$OUT/$p-before-$w.png"; echo "proof-shots: no main reference for $p@$w (new page)"; }
done; done
bak="$(mktemp -d)"; cp -a "$SHOTS/." "$bak/"; restore(){ rm -rf "$SHOTS"; mkdir -p "$SHOTS"; cp -a "$bak/." "$SHOTS/"; rm -rf "$bak"; }; trap restore EXIT
cd "$WEB"
[[ "${PROOF_SHOTS_SKIP_BUILD:-}" == 1 ]] || sh visual/build-web.sh >/dev/null
re="$(printf '%s|' "$@")"; re="(^| )(${re%|})\$"
npx playwright test --project=390 --project=1440 --update-snapshots=all -g "$re" --reporter=line || die "visual run failed (see output)"
for p in "$@"; do for w in "${WIDTHS[@]}"; do
  [[ -f "$SHOTS/$w/$p.png" ]] && cp "$SHOTS/$w/$p.png" "$OUT/$p-after-$w.png" || die "no after image for $p@$w"
done; done
table "$OUT" "$@"; echo "proof-shots: wrote $OUT/shots.md ($(( $# * 2 )) pairs)"
