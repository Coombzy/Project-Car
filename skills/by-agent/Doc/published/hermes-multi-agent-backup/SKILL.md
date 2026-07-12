---
name: hermes-multi-agent-backup
description: "Use when organizing, scheduling, or restoring Hermes backups across Doc/Porsche/McKing: daily/weekly/monthly local retention plus public git-safe inventories in Coombzy/Automation. Never commit secrets."
version: 1.0.0
author: Doc Hakosuka (adopted from Porsche fleet mutual-audit + backup protocol)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [backup, fleet, git-safe, retention, automation]
    related_skills: [fleet-mutual-audit, hermes-agent, github-repo-management]
---

# Hermes multi-agent backup

## Overview

Two layers per agent machine:

| Layer | Where | Git? |
|-------|-------|------|
| Full local | `backup/<Agent>/{daily,weekly,monthly}/` +/or Desktop archives | **No** (gitignored) |
| Git-safe | `backup/<Agent>/git-safe/` inventories | **Yes** (public-safe only) |

Canonical protocol: `Coombzy/Automation/backup/MUTUAL-AUDIT-PROTOCOL.md`  
Fleet layout: `Coombzy/Automation/backup/README.md`

## When to Use

- Daily 10pm backup jobs
- Mutual-audit re-export
- After major skill/config changes
- Restoring from local zip / deciding retention

## Doc machine recipe

Clone default: `~/hermes-tools/Automation`  
Script: `~/.hermes/scripts/daily-doc-backup.sh`

### Daily (local full/quick)

```bash
# quick critical state (includes sensitive files — LOCAL ONLY)
hermes backup --quick -o "$OUTDIR/hermes-quick-$STAMP.zip" -l "doc-daily"

# optional fuller zip (still local only)
# hermes backup -o "$OUTDIR/hermes-full-$STAMP.zip"
```

Retention targets (Doc-Todo): keep ~30 daily, promote weekly/monthly as needed.

### Git-safe (sanitized)

Rebuild inventory + `AUDIT-PACK.md` under `backup/Doc/git-safe/` (see `fleet-mutual-audit` skill).  
Never put `.env`, `auth.json`, tokens, or full profile tarballs in git.

### Schedule

- Target: `0 22 * * *` local (10pm)
- Prefer **launchd** or system cron on the host — not paid cloud agent cron for this
- Each machine runs **its own** job; jobs do not hop hosts

## Security

`Coombzy/Automation` is **public**. Ban list matches mutual-audit protocol.

## Common Pitfalls

1. Pushing `hermes backup` zips to GitHub.
2. Assuming Porsche’s cron runs on Doc.
3. Skipping git-safe re-export after big skill installs.
4. Storing PATs inside backup scripts.

## Verification

- [ ] Local archive exists under gitignored path
- [ ] No secrets staged for git
- [ ] launchd/cron loaded for 10pm
- [ ] Doc-Todo backup item updated when installed
