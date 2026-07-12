# Multi-Agent Hermes Backup Structure (Initial Implementation)

This reference captures the exact layout and script created during the July 2026 session for the Porsche / Doc Hudson / Lightning McKing team.

## Final Directory Tree
Porsche-backup/
├── agents/
│   ├── porsche/
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   ├── doc-hudson/
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   └── lightning-mcking/
│       ├── daily/
│       ├── weekly/
│       └── monthly/
├── logs/
├── scripts/
└── (root-level instruction files)

## Key Files Created
- `~/.hermes/scripts/daily-porsche-backup.sh` — the retention-aware backup script
- Cron entry: `0 2 * * * /Users/ben/.hermes/scripts/daily-porsche-backup.sh >> ~/.hermes/logs/...`

## Retention Logic Summary
- Daily backups always land in `agents/porsche/daily/`
- Files 31–90 days old are moved to `weekly/` only if they fall on a Monday
- Files >90 days old are moved to `monthly/` only if they are the 1st of the month
- All other files in the daily folder are deleted

The script is written to be portable (detects GNU vs BSD date) and safe to copy to the other two machines.