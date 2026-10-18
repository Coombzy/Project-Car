#!/bin/sh
# Print the pull request to merge, or one later.md line. Does not merge or wake a bot.
# usage: check-result.sh success|failure <pr> <branch>
conclusion=${1:-}
pr=${2:-}
branch=${3:-}
if [ "$conclusion" != "success" ] && [ "$conclusion" != "failure" ]; then
  echo "conclusion must be success or failure" >&2
  exit 2
fi
if [ -z "$pr" ] || [ -z "$branch" ]; then
  echo "pr and branch are required" >&2
  exit 2
fi
if [ "$conclusion" = "failure" ]; then
  printf '| Queue check failed on PR %s %s; leave the pull request open | proof | |\n' "$pr" "$branch"
  exit 0
fi
row=$(sh "$(dirname "$0")/next-row.sh")
if [ -z "$row" ]; then
  echo "no open row to move" >&2
  exit 2
fi
printf 'merge pull request %s %s\n' "$pr" "$branch"
printf 'move to Already on main: %s\n' "$row"
