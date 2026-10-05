# Macro Theme GitHub Write Rules — v1.3 (2026-10-05)

**Violating these is a process failure.** Same lesson as CCJ: full-file races overwrite living logs.

## Repository

- owner: `Coombzy`
- repo: `Project-Car`
- branch: `main` (protected — see write path below)
- prompt branch for this revision: `macro-prompt-v1.4`

## Before every write

1. `github___get_file_contents` on the **exact file** you will change. Capture `sha`.
2. **Log integrity check** before any prepend. If the body is the literal `PLACEHOLDER`, under ~500 characters, or has no `###` date header, refetch the raw blob. Do not prepend, and do not treat the log as empty, until the newest entry is visible. Never prepend onto a placeholder stub.
3. Write **immediately** after that read. Do not read other large files in between.
4. On SHA mismatch / 409 from a concurrent writer: **re-read SHA and retry once**. Then stop. Never loop.
5. A ruleset rejection (PR required, status checks) is **not** a SHA conflict. Do not retry `main`. Follow the protected-branch path once.

## Protected-branch path

`main` requires a pull request and status checks. If a direct write returns 409 / "Changes must be made through a pull request":

1. One branch from current `main` (do not open a second branch for the same run).
2. Put **both** the log update and the tracker update on that branch before opening the PR. Prompt/README edits use their own branch, not the analysis branch.
3. Open the PR into `main`. Report the PR URL and the commit SHA(s).
4. Do not report a file as committed if it was only drafted. Tracker rows that are not on the branch are not done.

## Living log (`finance/Macro_Theme_Log.md`)

- **Analysis:** prepend **one** new `### YYYY-MM-DD | HH:MM America/Regina` entry. Keep every older entry byte-for-byte.
- Never replace the file with a placeholder, summary, or truncated log.
- If today already has an official analysis entry, **or an open PR for today's `analysis_date`**, do not prepend a second full run. Overlap/addendum notes may be added **inside** today's newest entry only (do not rewrite older days).
- Compact: ranking scores (label them expected upside points, not a probability), mechanism, overlap scan, **industry analysis (before any ticker)**, then stock picks, proxies, falsifiers, sources. Comparison tables belong in the tracker.
- Do not list stock picks in an entry that lacks the industry block for that theme.
- Same cash-flow line = one ticker. Fewer than 3 picks with an explicit fail is success. Do not fill the slot.

## Tracker (`finance/Macro_Theme_Tracker.md`)

- One row per `(analysis_date, theme_id, proxy)`. `proxy` is the ticker — **stock pick or ETF**. Do not duplicate; update in place.
- Analysis: append rows with `status=open` and fill **spot_at_call**, **due_date**, **source_note**. `notes` starts with `pick` (single stock) or `basket` (ETF).
- `spot_at_call` must include the equity last print, the tell print, the source, and a timestamp. If two sources differ by more than 2%, widen the range or drop the name.
- Each kept theme should contribute up to **3 pick rows** plus any distinct basket overlay. If a pick *is* the proxy, one row only. Do not add a second ticker on the same cash-flow line to fill a slot.
- Do not change `pct_low` / `pct_high` / `horizon_days` on already-open rows (grading honesty). That includes illegal frozen horizons (the open 45-day TLT/XLF rows). New overlays / new picks get **new rows**. Do not "fix" old horizons.
- Grade at `due_date` ±1 trading day. Range hit is primary; direction is secondary. List past-due open rows before booking a new theme on the same tell. Do not open a new `theme_id` on that tell until the old row is graded or marked `expired`. An inverse is an overlay note unless the tell has actually flipped and the old row is flagged ungraded.

## Prompt / README

If an audit recommends a prompt change **or the user edits Macro Alpha**, apply it to `finance/Macro_Theme_Analysis_Prompt.md` in the same run (bump version + date) **and** bump this file / README if load-order or row contract changed. Leaving "exact prompt language" only in the Grok automation is a process miss.

## Single writer

If multiple agents are present, the **leader commits**. Others review in chat only.

## Do not add yet

- Calibration file (wait until first 14- or 30-day closes).
- Process Health table (optional after n>=3 runs).
