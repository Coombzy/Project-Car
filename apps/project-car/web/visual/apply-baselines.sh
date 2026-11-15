#!/bin/sh
# Compare screenshots to pngs stored from main's latest green visual run.
# When that cache is missing, or this pull request edits the committed pngs,
# leave the screenshots in the checkout. This does not build or render main.
set -eu
if [ -n "${VISUAL_DIR:-}" ]; then
  VISUAL=$VISUAL_DIR
else
  VISUAL=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
fi
BASE=$VISUAL/screenshot-baselines
SHOTS=$VISUAL/screenshots

if [ "${GITHUB_EVENT_NAME:-}" = "push" ]; then
  echo "push compares against the screenshots in this checkout"
  exit 0
fi

if [ -n "${SHOP_BASE_SHA:-}" ]; then
  changed=$(git -C "$VISUAL" diff --name-only --no-renames "$SHOP_BASE_SHA" HEAD || true)
  case "$changed" in
    *apps/project-car/web/visual/screenshots/*)
      echo "pull request edits screenshot baselines; comparing against the screenshots in this checkout"
      exit 0
      ;;
  esac
fi

if [ ! -d "$BASE" ]; then
  echo "no stored screenshot baseline; comparing against the screenshots in this checkout"
  exit 0
fi
found=$(find "$BASE" -name '*.png' -type f -print -quit)
if [ -z "$found" ]; then
  echo "no stored screenshot baseline; comparing against the screenshots in this checkout"
  exit 0
fi

echo "comparing against stored screenshot baselines from main"
find "$BASE" -name '*.png' -type f | while IFS= read -r png; do
  rel=${png#"$BASE"/}
  dest=$SHOTS/$rel
  mkdir -p "$(dirname "$dest")"
  cp "$png" "$dest"
done
