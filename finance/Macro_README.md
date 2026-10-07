# Macro Industry Theme Map Process

Owner: `Coombzy/Project-Car`  
Current versions: **Analysis v1.6** · **Write rules v1.4** (2026-10-06)  
Grok automation: **Macro Alpha** (weekly Mon/Thu 07:30 America/Regina)  
Not financial advice. Selection support only — no position sizes.

## Load order (every run)

1. `finance/Macro_WRITE_RULES.md`
2. `finance/Macro_Theme_Analysis_Prompt.md` (must be **v1.6+**; check Version + Last edited; quote Version, ref, and blob SHA in the run header and in any chat answer that uses the gates)
3. `finance/Macro_Theme_Log.md` — newest 1–2 entries. If the body is `PLACEHOLDER`, under ~500 characters, or has no `###` date header, refetch the raw blob. If it is still `PLACEHOLDER`, replace the stub once. Do not prepend onto it.
4. `finance/Macro_Theme_Tracker.md` — **all open rows** + last 5 closed (when any exist). Past-due rows are status-edited in the same PR, not only listed in chat.

If GitHub prompt and the Macro Alpha wrapper disagree, **GitHub v1.6+ wins** except the wrapper's must-keep user constraints (already merged): rank by upside × chance, prefer liquid single stocks, up to 3 names per theme, **industry analysis before picks**.

## What v1.6 changed

- Ad-hoc "what are the plays" answers use a short form (tell, one URL, 52-week and 12-month already-priced check, one horizon, one falsifier) and do not book unless asked.
- A 52-week high on this tell fails already-priced even if the tracker has no row. "Not an open row" is not a screen. The 150% / 12-month rule is an extra cut, not the only one.
- An inventory level needs the EIA weekly table URL. A portal draw is not a stock level.
- Two clocks on one tell get one horizon per name. A 14-day cost relief and a 60-day residual long are not the same trade.
- An inverse inside the parent horizon is one `overlay` row, parent ranges frozen, and it does not use a theme slot. A prose note with zero rows cannot be graded.
- If the log is still `PLACEHOLDER` after a refetch, replace the stub once. Do not prepend onto it.
- Chat answers that use the gates quote Version, ref, and blob SHA.

## What v1.5 changed

- Past-due rows are marked `expired-ungraded` (or graded) in the tracker. A chat-only list is a miss. After that flag, a flipped tell may be a new `theme_id`.
- Score floor of 5 applies to the pre-haircut score only. Haircut is shown and changes action.
- A 0-theme day is an official log entry. Top dropped candidate with pre-haircut ≥ 5 gets a shadow industry block, no pick rows.
- Run header quotes Version, ref, and blob SHA actually read.

## What v1.4 changed

- Log integrity gate and protected-branch path: on 409, one branch, log and tracker both on that branch, then a PR.
- Same cash-flow line = one ticker. Fewer than 3 picks with an explicit fail is success.
- Score is labeled expected upside points.
- `spot_at_call` requires equity last print, tell print, source, and timestamp. Falsifier must be a number checkable before `due_date`.

## What v1.3 changed

- For each kept theme, write **Industry analysis** before any ticker. The stock picks are the output of that screen.

## What v1.2 changed (from Macro Alpha)

- Rank candidate themes by `(conf/100) × pct_high` of the best benefit name; keep top 3.
- Prefer liquid single stocks (NYSE/Nasdaq/TSX, not OTC).
- Horizons on new rows: **14 / 30 / 60 / 90** (not 45). Do not rewrite old 45-day rows.

## Cadence (intended)

| Job | When | Why |
|-----|------|-----|
| Analysis (Macro Alpha) | Mon + Thu 07:30 America/Regina | ~72h window; max 3 themes |
| Grade | Each open row at `due_date` ±1 session, and status-edit past-due rows in the same PR as the next run | Fill actual_pct / hit_range / hit_dir; set closed, expired-ungraded, or falsified |

## One-writer rule

Only **one** agent commits per job. Team review is fine; racing writes is how overwrites happen.

## Related

CCJ daily process is separate (`CCJ_README.md`). Do not mix CCJ tracker rows into this file.
