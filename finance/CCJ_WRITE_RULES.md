# CCJ GitHub Write Rules — v1.0 (2026-08-24)

**Violating these is a process failure** (Audit Score -1). The Jul 23 overwrite and the Aug 24 Process Health miss both came from full-file races.

## Repository

- owner: `Coombzy`
- repo: `Project-Car`
- branch: `main`

## Before every write

1. `github___get_file_contents` on the **exact file** you will change. Capture `sha`.
2. Write **immediately** after that read. Do not read other large files in between.
3. On SHA mismatch / 409 / "another agent already completed": **re-read SHA and retry once**. Then stop. Never loop.

## Living log (`finance/CCJ_Daily_Metrics_Audit_Log.md`)

- **Analysis:** prepend **one** new `### YYYY-MM-DD | HH:MM TZ` entry. Keep every older entry byte-for-byte.
- **Audit:** replace **only** the newest entry's `#### Audit / Reviewer Notes` block (the placeholder). Do not rewrite older audits. Do not nest "Post-Performance Audit Update" inside historical entries — put closed-horizon results in `CCJ_Prediction_Tracker.md`.
- **Never** replace the file with a placeholder, summary, or truncated log.
- If today already has an **EOD** analysis entry, do not prepend a second one. If today has only an incomplete early snapshot, you may **replace that snapshot in place** with the EOD version (same heading date).
- New Audit Notes should stay compact (<= 80 lines). Comparison tables belong in the tracker.

## Process Health (`finance/CCJ_Process_Health.md`)

- Prepend **one** table row. Do not drop existing rows.
- Analysis row: `Date | Confidence | (pending) | note | Yes/Fallback`
- Audit row: overwrite that same date's Audit Score cell **or** prepend a new dated row if none exists.
- After commit, re-read the file and **confirm the new date is present**. If not, retry once. Do not claim success without that confirmation.

## Prediction tracker (`finance/CCJ_Prediction_Tracker.md`)

- Analysis: append rows for the four new horizons (`status=open`).
- Audit: update `actual_*`, `hit`, `directional`, `pct_error`, `status` (`preliminary` during RTH, `closed` after regular-session close).
- Do not duplicate a (`analysis_date`, `horizon`) pair; update in place.

## Prompt files

If an audit recommends a prompt change, **apply it to the prompt file in the same run** (bump the version + date). Leaving "exact prompt language" only in the log is a process miss.

## Single writer

If multiple agents are present, the **leader commits**. Others review in chat only.
