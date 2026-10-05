# Macro Theme GitHub Write Rules — v1.3 (2026-10-05)

**Violating these is a process failure.** Same lesson as CCJ: full-file races overwrite living logs. 2026-10-05 lesson: a truncated `PLACEHOLDER` read plus a ruleset 409 left tracker rows off the branch.

## Repository

- owner: `Coombzy`
- repo: `Project-Car`
- branch: `main` (write here if allowed)
- if `main` rejects the push: one branch `macro-theme-YYYYMMDD` or `macro-prompt-vX.Y`, then a pull request into `main`

## Before every write

1. `github___get_file_contents` on the **exact file** you will change. Capture blob `sha`.
2. **Log gate.** If `finance/Macro_Theme_Log.md` body is the literal `PLACEHOLDER`, is under ~500 characters, or has no `###` date header, refetch the raw blob. Do not prepend until the newest entry is visible. Never replace the file with a placeholder, summary, or truncated log.
3. Write **immediately** after that read. Do not read other large files in between.
4. On SHA mismatch / 409 conflict / "another agent already completed": **re-read SHA and retry once**. Then stop. Never loop.
5. A ruleset 409 (PR required, status checks) is **not** a SHA conflict. Do not retry the same write to `main`. One branch, both files on that branch, then open a PR. Report the PR URL and both commit SHAs. Do not say the tracker was committed if it was only drafted.

## Living log (`finance/Macro_Theme_Log.md`)

- **Analysis:** prepend **one** new `### YYYY-MM-DD | HH:MM TZ` entry. Keep every older entry byte-for-byte.
- If today already has an official analysis entry, or an open PR for that `analysis_date`, do not prepend a second full run. Overlap/addendum notes may be added **inside** today's newest entry only (do not rewrite older days).
- Compact: ranking scores (label them **expected upside points**, not a probability), mechanism, overlap scan, **industry analysis (before any ticker)**, then stock picks, proxies, falsifiers, sources. Comparison tables belong in the tracker.
- Do not list stock picks in an entry that lacks the industry block for that theme.
- End the chat report with `rows appended: N` and the commit SHA or PR URL.

## Tracker (`finance/Macro_Theme_Tracker.md`)

- One row per `(analysis_date, theme_id, proxy)`. `proxy` is the ticker — **stock pick or ETF**. Do not duplicate; update in place.
- Analysis: append rows with `status=open` and fill **spot_at_call**, **due_date**, **source_note**. `notes` starts with `pick` (single stock) or `basket` (ETF).
- `spot_at_call` must include the equity last print **and** the tell print, plus source and timestamp (e.g. `JBHT 234.20 Fri 2026-10-02; ULSD 4.56 / crack ~70, ING 2026-10-05`). Driver-only is allowed only for an ETF with no clean print.
- Each kept theme should contribute up to **3 pick rows** plus any distinct basket overlay. Same cash-flow line = one ticker. Fewer than 3 with an explicit screen fail is success. If a pick *is* the proxy, one row only.
- Do not change `pct_low` / `pct_high` / `horizon_days` on already-open rows (grading honesty). That includes illegal 45-day rows. New overlays / new picks get **new rows**.
- **Grade before new themes.** List every open row with `due_date` <= today. Grade in place if a price is in hand (fill `actual_pct`, `hit_range`, `hit_dir`, `graded_date`, `status=closed` or `falsified`). If no price, set `status=expired-ungraded` and do not touch ranges. Do not open a new `theme_id` on the same tell until that row is graded or marked `expired-ungraded`. An inverse of an open row is an overlay note, not a new id.
- Grade at `due_date` ±1 trading day. Range hit is primary; direction is secondary.

## Prompt / README

If an audit recommends a prompt change **or the user edits Macro Alpha**, apply it to `finance/Macro_Theme_Analysis_Prompt.md` in the same run (bump version + date) **and** bump this file / README if load-order or row contract changed. Leaving "exact prompt language" only in the Grok automation is a process miss.

## Single writer

If multiple agents are present, the **leader commits**. Others review in chat only. Do not parallel-call `github___create_or_update_file` on the same path.

## Do not add yet

- Calibration file (wait until first 14- or 30-day closes).
- Process Health table (optional after n>=3 runs).
