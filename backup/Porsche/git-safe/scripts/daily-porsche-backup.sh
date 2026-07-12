#!/bin/bash
# Multi-Agent Hermes Backup + Retention Script (Porsche)
# Structure:
#   agents/porsche/daily/     - last 30 days
#   agents/porsche/weekly/    - one per week (days 31-90)
#   agents/porsche/monthly/   - one per month (>90 days)
#
# Same structure exists for doc-hudson and lightning-mcking

set -e

AGENT="porsche"
BACKUP_ROOT="/Users/ben/Desktop/Porsche-backup/agents/$AGENT"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_ROOT/daily/hermes-$AGENT-backup-$DATE.tar.gz"
PROFILE="default"

# Ensure directories exist
mkdir -p "$BACKUP_ROOT"/{daily,weekly,monthly}

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting daily backup for $AGENT..."

# Create today's backup in daily/
hermes profile export "$PROFILE" -o "$BACKUP_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup created: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"

# ============================================
# RETENTION LOGIC
# ============================================

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Applying retention policy for $AGENT..."

if date --version 2>/dev/null | grep -q GNU; then
    THIRTY_DAYS_AGO=$(date -d "30 days ago" +%Y-%m-%d)
    NINETY_DAYS_AGO=$(date -d "90 days ago" +%Y-%m-%d)
else
    THIRTY_DAYS_AGO=$(date -v-30d +%Y-%m-%d)
    NINETY_DAYS_AGO=$(date -v-90d +%Y-%m-%d)
fi

echo "  - Daily:   last 30 days (>$THIRTY_DAYS_AGO)"
echo "  - Weekly:  31-90 days"
echo "  - Monthly: >90 days"

# Helper to move or keep a file
process_backup() {
    local file=$1
    local filename=$(basename "$file")
    local file_date=${filename#hermes-$AGENT-backup-}
    file_date=${file_date%.tar.gz}

    # Always keep today's backup
    if [[ "$file_date" == "$DATE" ]]; then
        return 0
    fi

    if [[ "$file_date" > "$THIRTY_DAYS_AGO" ]]; then
        # Keep in daily/
        return 0
    elif [[ "$file_date" > "$NINETY_DAYS_AGO" ]]; then
        # Weekly window - keep only Mondays in weekly/
        local dow
        if date --version 2>/dev/null | grep -q GNU; then
            dow=$(date -d "$file_date" +%u)
        else
            dow=$(date -j -f "%Y-%m-%d" "$file_date" +%u)
        fi
        if [[ "$dow" == "1" ]]; then
            mv -n "$file" "$BACKUP_ROOT/weekly/" 2>/dev/null || true
        else
            rm -f "$file"
        fi
    else
        # Monthly window - keep only 1st of month in monthly/
        local dom
        if date --version 2>/dev/null | grep -q GNU; then
            dom=$(date -d "$file_date" +%d)
        else
            dom=$(date -j -f "%Y-%m-%d" "$file_date" +%d)
        fi
        if [[ "$dom" == "01" ]]; then
            mv -n "$file" "$BACKUP_ROOT/monthly/" 2>/dev/null || true
        else
            rm -f "$file"
        fi
    fi
}

# Process daily folder
for f in "$BACKUP_ROOT/daily"/hermes-$AGENT-backup-*.tar.gz; do
    [ -f "$f" ] && process_backup "$f"
done

# Also clean up weekly and monthly folders if they have old non-qualifying files
# (simple approach: just leave them; the move logic above is the main filter)

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Retention complete for $AGENT"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Daily backup job finished."