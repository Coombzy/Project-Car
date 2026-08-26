# Macro Theme GitHub Write Rules — v1.1 (2026-08-26)

**Violating these is a process failure.** Same lesson as CCJ: full-file races overwrite living logs.

## Repository

- owner: `Coombzy`
- repo: `Project-Car`
- branch: `main`

## Before every write

1. `github___get_file_contents` on the **exact file** you will change. Capture `sha`.
2. Write **immediately** after that read. Do not read other large files in between.
3. On SHA mismatch / 409 / "another agent already completed": **re-read SHA and retry once**. Then stop. Never loop.

## Living log (`finance/Macro_Theme_Log.md`)

- **Analysis:** prepend **one** new `### YYYY-MM-DD | HH:MM TZ` entry. Keep every older entry byte-for-byte.
- Never replace the file with a placeholder, summary, or truncated log.
- If today already has an official analysis entry, do not prepend a second full run. Overlap/addendum notes may be added **inside** today's newest entry only (do not rewrite older days).
- Compact: ranking scores, mechanism, overlap scan, 3 stock picks, proxies, falsifiers, sources. Comparison tables belong in the tracker.

## Tracker (`finance/Macro_Theme_Tracker.md`)

- One row per `(analysis_date, theme_id, proxy)`. `proxy` is the ticker — **stock pick or ETF**. Do not duplicate; update in place.
- Analysis: append rows with `status=open` and fill **spot_at_call**, **due_date**, **source_note**. `notes` starts with `pick` (single stock) or `basket` (ETF).
- v1.2: each kept theme should contribute up to **3 pick rows** plus any distinct basket overlay. If a pick *is* the proxy, one row only.
- Do not change `pct_low` / `pct_high` / `horizon_days` on already-open rows (grading honesty). New overlays / new picks get **new rows**.
- Grade at `due_date` ±1 trading day. Range hit is primary; direction is secondary.

## Prompt / README

If an audit recommends a prompt change **or the user edits Macro Alpha**, apply it to `finance/Macro_Theme_Analysis_Prompt.md` in the same run (bump version + date) **and** bump this file / README if load-order or row contract changed. Leaving "exact prompt language" only in the Grok automation is a process miss.

## Single writer

If multiple agents are present, the **leader commits**. Others review in chat only.

## Do not add yet

- Calibration file (wait until first 14- or 30-day closes).
- Process Health table (optional after n>=3 runs).
