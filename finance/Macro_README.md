# Macro Industry Theme Map Process

Owner: `Coombzy/Project-Car`  
Current versions: **Analysis v1.4** · **Write rules v1.3** (2026-10-05)  
Grok automation: **Macro Alpha** (weekly Mon/Thu 07:30 America/Regina)  
Not financial advice. Selection support only — no position sizes.

## Load order (every run)

1. `finance/Macro_WRITE_RULES.md`
2. `finance/Macro_Theme_Analysis_Prompt.md` (must be **v1.4+**; check Version + Last edited)
3. `finance/Macro_Theme_Log.md` — newest 1–2 entries. If the body is `PLACEHOLDER`, under ~500 characters, or has no `###` date header, refetch the raw blob before treating the log as empty.
4. `finance/Macro_Theme_Tracker.md` — **all open rows** + last 5 closed (when any exist). List past-due open rows before booking a new theme on the same tell.

If GitHub prompt and the Macro Alpha wrapper disagree, **GitHub v1.4+ wins** except the wrapper's must-keep user constraints (already merged): rank by upside × chance, prefer liquid single stocks, up to 3 names per theme, **industry analysis before picks**.

## What v1.4 changed

- Log integrity gate: do not prepend onto a `PLACEHOLDER` or truncated body. Skip a second official run if today already has a v1.4 header or an open PR for that `analysis_date`.
- Protected `main`: on 409, one branch, log and tracker both on that branch, then a PR. Do not report a drafted tracker as committed.
- Grade-before-new-theme on the same tell. Do not edit frozen ranges or illegal 45-day horizons. An inverse of an open theme is an overlay unless the tell has flipped and the old row is flagged ungraded.
- Same cash-flow line = one ticker. Fewer than 3 picks with an explicit fail is success.
- Score is labeled expected upside points. Floor: best benefit score under 5 after a priced-in haircut → 0 themes.
- `spot_at_call` requires equity last print, tell print, source, and timestamp. Falsifier must be a number checkable before `due_date`.

## What v1.3 changed

- For each kept theme, write **Industry analysis** (value chain, transmission/tell, 5–8 peer universe, screen, hurt side, already-priced) **before any ticker**.
- The stock picks are the *output* of that screen, not the starting point.

## What v1.2 changed (from Macro Alpha)

- Rank candidate themes by `(conf/100) × pct_high` of the best benefit name; keep top 3.
- Prefer **single stocks** with large expected % moves (NYSE/Nasdaq/TSX, not OTC).
- Output up to **3 stock picks per theme**. Picks with ranges are tracker rows (`notes` = `pick`). ETFs = `basket`.
- Horizons allowed on **new** rows: **14 / 30 / 60 / 90** (not 45). Do not rewrite old 45-day rows.

## Cadence (intended)

| Job | When | Why |
|-----|------|-----|
| Analysis (Macro Alpha) | Mon + Thu 07:30 America/Regina | ~72h window; max 3 themes |
| Grade | Each open row at `due_date` ±1 session, and list past-due rows before a new same-tell theme | Fill actual_pct / hit_range / hit_dir; set closed, expired, or falsified |

## One-writer rule

Only **one** agent commits per job. Team review is fine; racing writes is how overwrites happen.

## Related

CCJ daily process is separate (`CCJ_README.md`). Do not mix CCJ tracker rows into this file.
