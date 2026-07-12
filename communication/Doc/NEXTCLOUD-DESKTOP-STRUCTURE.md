# TEMPORARY HANDOFF — Doc Nextcloud host + desktop structure

**Status:** OPEN until Doc confirms structure created  
**Owner:** Doc Hakosuka  
**Decision (Ben, 2026-07-12):** Doc is the **Nextcloud server host** (1TB drive vs Porsche 500GB).  
**Done token:** `DOC_NEXTCLOUD_STRUCTURE_READY` + path confirmation  

Porsche remains **travel / edge PA**. McKing later = bulk storage/backups, not first Nextcloud host.

---

## 1. Create this tree on Doc’s Desktop

Run on **Doc** (M1 Max):

```bash
BASE="$HOME/Desktop/Fleet-Nextcloud"
mkdir -p \
  "$BASE/Memory/Shared" \
  "$BASE/Memory/Porsche" \
  "$BASE/Memory/Doc" \
  "$BASE/Memory/McKing" \
  "$BASE/Memory/Dreams/Porsche" \
  "$BASE/Memory/Dreams/Doc" \
  "$BASE/Memory/Dreams/McKing" \
  "$BASE/Heartbeats/MissionControl" \
  "$BASE/Heartbeats/Fleet" \
  "$BASE/Handoffs/active" \
  "$BASE/Handoffs/archive" \
  "$BASE/Docs" \
  "$BASE/Inbox" \
  "$BASE/Outbox" \
  "$BASE/Backups/git-safe-notes" \
  "$BASE/Templates"

# Seed READMEs (idempotent)
cat > "$BASE/README.md" <<'EOF'
# Fleet-Nextcloud (Doc host)

Ben decision 2026-07-12: **Doc** hosts Nextcloud (1TB). This Desktop tree is the
**starting layout** before/while Nextcloud Docker is stood up.

Later: bind or sync this tree (or an equivalent path) into the Nextcloud data
volume / external storage so agents use WebDAV/OCS against the same folders.

## Layout

| Path | Purpose |
|------|---------|
| `Memory/` | Medium/long-term fleet memory (not public GitHub) |
| `Memory/Shared/` | Cross-agent facts, decisions, glossary |
| `Memory/Porsche|Doc|McKing/` | Per-agent notes (specialists stay thin) |
| `Memory/Dreams/` | Dream-cron digests (consolidation logs) |
| `Heartbeats/` | MC + fleet heartbeat notes |
| `Handoffs/active|archive` | Porsche→Doc/McKing work packets |
| `Docs/` | Optional mirror of specs (canonical still skill+GitHub Docs/) |
| `Inbox/` | Human/agent drop zone |
| `Outbox/` | Staged exports to GitHub (public-safe only) |
| `Backups/git-safe-notes` | Non-secret inventory notes only |
| `Templates/` | HANDOFF / dream templates |

## Rules

- **No secrets** (`.env`, tokens, 2FA, full profile tarballs) in this tree if it will sync to devices you don't fully trust.
- **Public git** stays for process (todos, catalogs). Personal/fleet memory lives here.
- Porsche writes orchestration memory + HANDOFFs; Doc/McKing write **results**, not dual Ben biographies.
EOF

cat > "$BASE/Memory/_index.md" <<'EOF'
# Fleet memory index

- **Hot:** each agent MEMORY.md / USER.md (Hermes built-in, small)
- **Warm/cold:** this Nextcloud tree (Doc host)
- **Process SSOT:** `Coombzy/Automation` (public) — todos, catalogs, protocols

Porsche owns medium/long-term Ben+fleet continuity. Doc/McKing keep thin host memory and follow HANDOFFs.
EOF

cat > "$BASE/Templates/HANDOFF.md" <<'EOF'
# HANDOFF | <from> → <to> | <date>

**Done-when:** …
**Priority:** P0|P1|P2

## Goal
## Non-goals
## Paths
## Acceptance checks
## Model hint
## Links (Nextcloud / GitHub)
EOF

cat > "$BASE/Templates/DREAM-DIGEST.md" <<'EOF'
# Dream digest | <agent> | YYYY-MM-DD

## What happened (last window)
## Decisions
## Open loops (owner)
## MEMORY.md changes suggested (hot)
## Nextcloud writes (this file + any)
## HANDOFFs to open (if any)
## Silent? (nothing important)
EOF

# Empty keepers
touch \
  "$BASE/Memory/Shared/.gitkeep" \
  "$BASE/Memory/Porsche/.gitkeep" \
  "$BASE/Memory/Doc/.gitkeep" \
  "$BASE/Memory/McKing/.gitkeep" \
  "$BASE/Handoffs/active/.gitkeep" \
  "$BASE/Handoffs/archive/.gitkeep" \
  "$BASE/Inbox/.gitkeep" \
  "$BASE/Outbox/.gitkeep"

echo "Created: $BASE"
find "$BASE" -type d | sort
```

### Verify
```bash
ls -la ~/Desktop/Fleet-Nextcloud
test -d ~/Desktop/Fleet-Nextcloud/Memory/Dreams/Doc && echo OK
```

---

## 2. Reply when done

In `#tire-shop`:

```text
DOC_NEXTCLOUD_STRUCTURE_READY
path: /Users/dochak/Desktop/Fleet-Nextcloud   # or actual path
disk: 1TB host confirmed for NC role
```

---

## 3. Next (not this handoff — later)

- Install Nextcloud (Docker on Doc or native) with data dir pointing at large volume  
- Expose via Tailscale only first; no public internet without Ben OK  
- Wire agents WebDAV later (Porsche primary writer for Memory/)  
- McKing becomes **backup receive** target when online, not first NC host  

---

## 4. Related git files

| File | Purpose |
|------|---------|
| This file | Structure instructions |
| `communication/Doc/DREAM-CRON.md` | Doc dreaming cron — install on Doc |
| `communication/Porsche/DREAM-CRON.md` | Porsche dreaming cron (orchestrator) |

— Porsche for Ben
