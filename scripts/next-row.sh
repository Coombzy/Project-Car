#!/bin/sh
# Print the first open row under Now. An empty Now prints nothing.
# Does not merge, deploy, or wake a bot.
file=Docs/queue.md
if [ ! -f "$file" ]; then
  echo "no queue" >&2
  exit 1
fi
awk '
  /^## Now[[:space:]]*$/ { p = 1; next }
  /^## / { if (p) exit }
  p {
    line = $0
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
    if (line == "") next
    if (line == "No open row" || line == "No open row.") exit
    print line
    exit
  }
' "$file"
