# Doc dream cron — specialist / host consolidation (thin)

**Role lock:** Doc = heavy compute / local LLM / implementer.  
**Not** a second PA. Do **not** dream Ben’s full life story or own fleet todos.

**Created:** 2026-07-12  
**Install on:** Doc host only  
**Canonical prompt:** section below (self-contained for cron)

---

## Goals of Doc’s dream

1. Consolidate **host / specialist** facts (Ollama, disk, failed jobs, local routing).  
2. Write a short digest under Nextcloud (or Desktop fallback):  
   `~/Desktop/Fleet-Nextcloud/Memory/Dreams/Doc/YYYY-MM-DD.md`  
3. Optionally refresh thin Hermes MEMORY (host-only) — never inflate USER into dual-PA.  
4. Scan `Handoffs/active/` for Doc-owned work; if blocked, note one line for Porsche.  
5. **Silent** Discord if nothing important (no empty “I dreamed”).

---

## Schedule (recommended)

```text
30 23 * * 1,3,5
```

Mon/Wed/Fri **23:30 local** (after day work; low interrupt).  
Adjust timezone to Doc machine local.

Prefer **local model** for the job when configured; otherwise main model with tight scope.

---

## Install on Doc

```bash
cd /Users/dochak/hermes-tools/Automation   # or your clone
git pull --ff-only origin main

# Read this file, then create cron (example via CLI — adapt to hermes cron create UX):
# Or ask Hermes in #doc-garage:
#   "Create dream cron from communication/Doc/DREAM-CRON.md"
```

Using Hermes agent (preferred):

1. Open `#doc-garage` or CLI on Doc.  
2. Say: **Install the Doc dream cron from `communication/Doc/DREAM-CRON.md` in Automation — use the prompt and schedule there.**  
3. Confirm with `hermes cron list` (or tool equivalent).  
4. Ensure Nextcloud desktop tree exists first (`NEXTCLOUD-DESKTOP-STRUCTURE.md`).

### Cron fields

| Field | Value |
|-------|--------|
| name | `doc-dream-specialist` |
| schedule | `30 23 * * 1,3,5` |
| skills | `token_preflight`, `project-car` (optional), `xai-model-selection` |
| deliver | `discord:#doc-garage` or tire-shop **only if non-empty report** |
| workdir | Automation clone path on Doc |
| enabled | true after structure exists |

If Hermes cron cannot suppress empty delivery, end with a single line `DREAM_SILENT` and configure yourself to ignore, or deliver `local` only until we have a silent path.

---

## Prompt (paste into cron `prompt` — self-contained)

```text
You are Doc Hakosuka running the scheduled **specialist dream** job (offline consolidation).

CHARTER LOCK: You are specialist / heavy compute / local LLM implementer on M1 Max 64GB. You are NOT Porsche (PA/coordinator). Do not own Ben's day-to-day todos. Do not become dual-PA. Thin memory only.

## Done-when
1. Write dream digest to:
   - Prefer: ~/Desktop/Fleet-Nextcloud/Memory/Dreams/Doc/YYYY-MM-DD.md
   - Fallback: ~/Desktop/Doc-Dreams/YYYY-MM-DD.md if Fleet-Nextcloud missing (note blocker)
2. Optionally consolidate Hermes MEMORY.md host-only facts (Ollama models, bind localhost, always-on). Do NOT rewrite USER.md into a Ben PA profile.
3. Check ~/Desktop/Fleet-Nextcloud/Handoffs/active/ for Doc-owned packets; if any, list status (not started / in progress / blocked).
4. If nothing material: write digest with "## Silent" and do not ping fleet with noise. Final response may be: DREAM_SILENT
5. Never commit secrets. Never put .env / tokens / serials in digests.

## Steps
1. Restate charter in one line.
2. Gather cheap host signals (timeouts short):
   - date, disk free on home/Desktop
   - ollama list if available (5s timeout)
   - whether Fleet-Nextcloud tree exists
   - list Handoffs/active filenames only
3. session_search only if needed for Doc technical decisions last few days — not Ben life history.
4. Write digest using template sections:
   - What happened (host/work)
   - Local LLM / routing notes
   - Open implement loops
   - MEMORY.md host tweaks (if any)
   - Handoffs status
   - Asks for Porsche (max 3 bullets, only if real)
5. Keep digest under ~80 lines. Prefer facts over prose.
6. Final response: path to digest + one-line summary, or DREAM_SILENT.

## Anti-goals
- No skill-count parity work
- No full mutual-audit unless scheduled separately
- No inventing Nextcloud Docker install in this job (structure only)
- No public git push of private digests
```

---

## Verify

```bash
hermes cron list   # show doc-dream-specialist
# After first fire:
ls -la ~/Desktop/Fleet-Nextcloud/Memory/Dreams/Doc/
```

Reply in `#tire-shop` when installed:

```text
DOC_DREAM_CRON_INSTALLED
schedule: 30 23 * * 1,3,5
```

— Porsche for Ben
