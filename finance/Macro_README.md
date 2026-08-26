# Macro Industry Theme Map Process

Owner: `Coombzy/Project-Car`  
Current versions: **Analysis v1.2** · **Write rules v1.1** (2026-08-26)  
Grok automation: **Macro Alpha** (weekly Mon/Thu 07:30 America/Regina)  
Not financial advice. Selection support only — no position sizes.

## Load order (every run)

1. `finance/Macro_WRITE_RULES.md`
2. `finance/Macro_Theme_Analysis_Prompt.md` (must be **v1.2+**; check Version + Last edited)
3. `finance/Macro_Theme_Log.md` — newest 1–2 entries
4. `finance/Macro_Theme_Tracker.md` — **all open rows** + last 5 closed (when any exist)

If GitHub prompt and the Macro Alpha wrapper disagree, **GitHub v1.2+ wins** except the wrapper's must-keep user constraints (already merged into v1.2): rank by upside × chance, prefer liquid single stocks, 3 names per theme.

## What v1.2 changed (from Macro Alpha)

- Rank candidate themes by `(conf/100) × pct_high` of the best benefit name; keep top 3.
- Prefer **single stocks** with large expected % moves (NYSE/Nasdaq/TSX, not OTC).
- Output **3 stock picks per theme**. Picks with ranges are tracker rows (`notes` = `pick`). ETFs = `basket`.
- Horizons allowed: **14 / 30 / 60 / 90** (not 45).

## Cadence (intended)

| Job | When | Why |
|-----|------|-----|
| Analysis (Macro Alpha) | Mon + Thu 07:30 America/Regina | ~72h window; max 3 themes |
| Grade | Each open row at `due_date` ±1 session | Fill actual_pct / hit_range / hit_dir; set closed or falsified |

## One-writer rule

Only **one** agent commits per job. Team review is fine; racing writes is how overwrites happen.

## Related

CCJ daily process is separate (`CCJ_README.md`). Do not mix CCJ tracker rows into this file.
