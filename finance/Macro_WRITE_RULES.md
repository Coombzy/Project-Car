# Macro Theme GitHub Write Rules — v1.4 (2026-10-06)

**Violating these is a process failure.** Same lesson as CCJ: full-file races overwrite living logs.

## Repository

- owner: `Coombzy`
- repo: `Project-Car`
- branch: `main` (protected — see write path below)
- prompt branch for this revision: `macro-prompt-v1.4` (open PR)

## Before every write

1. `github___get_file_contents` on the **exact file** you will change. Capture `sha`.
2. **Log integrity check.** If the body is the literal `PLACEHOLDER`, under ~500 characters, or has no `###` date header, refetch the raw blob. If it is still `PLACEHOLDER`, **replace the stub once** with the new entry. Do not prepend onto a placeholder. Do not treat a placeholder as empty history.
3. Write **immediately** after that read. Do not read other large files in between.
4. On SHA mismatch / 409 from a concurrent writer: **re-read SHA and retry once**. Then stop. Never loop.
5. A ruleset rejection (PR required, status checks) is **not** a SHA conflict. Do not retry `main`. Follow the protected-branch path once.

## Protected-branch path

`main` requires a pull request and status checks. If a direct write returns 409 / "Changes must be made through a pull request":

1. One branch from current `main` (do not open a second branch for the same run).
2. Put **both** the log update and the tracker update on that branch before opening the PR. Prompt/README edits use their own branch, not the analysis branch.
3. Open the PR into `main`. Report the PR URL and the commit SHA(s).
4. Do not report a file as committed if it was only drafted. Tracker rows that are not on the branch are not done.
5. A 0-theme day still takes this path. `rows appended: 0` is valid. Past-due status edits count as tracker writes and must be on the branch.

## Living log (`finance/Macro_Theme_Log.md`)

- **Analysis:** prepend **one** new `### YYYY-MM-DD | HH:MM America/Regina` entry. Keep every older entry byte-for-byte. If the file is `PLACEHOLDER`, replace the stub once instead of prepending.
- Never replace a real log with a placeholder, summary, or truncated log.
- First line of the entry quotes the prompt Version, ref, and blob SHA actually read.
- If `main` already has an official analysis entry for today, **or an open PR for today's `analysis_date`**, do not prepend a second full run. A branch-only entry with no open PR is not an official entry.
- A 0-theme day is an official entry. It includes the driver snapshot, past-due actions, ranking with pre- and post-haircut scores, and a shadow industry block for the top dropped candidate if its pre-haircut score is ≥ 5.
- Do not list stock picks in an entry that lacks the industry block for that theme.
- Ad-hoc "what are the plays" answers do not write the log unless the user asked to book.

## Tracker (`finance/Macro_Theme_Tracker.md`)

- One row per `(analysis_date, theme_id, proxy)`. Do not duplicate; update in place.
- `notes` starts with `pick`, `basket`, or `overlay`.
- `spot_at_call` must include the equity last print, the tell print, a source URL, and a timestamp. If two sources differ by more than 2%, quote both and widen or drop. Do not silently average. Label futures vs retail.
- An inventory level requires the EIA Weekly Petroleum Status Report table URL. A portal draw is not a stock level.
- An inverse still inside its horizon is **one overlay row**. It does not count toward the 3-theme cap. Parent ranges stay frozen. A prose note with zero rows cannot be graded.
- Do not change `pct_low` / `pct_high` / `horizon_days` on already-open rows, including illegal frozen 45-day rows.
- If `due_date` < analysis_date, set `status=expired-ungraded` in this file unless a closing print is in hand. A chat-only past-due list is a process miss.
- After a row is `expired-ungraded` or `closed` and the tell has flipped, a new `theme_id` on that tell is allowed.
- Ad-hoc play answers do not append rows unless the user asked to book.

## Prompt / README

If an audit recommends a prompt change, apply it to `finance/Macro_Theme_Analysis_Prompt.md` (bump version + date) and bump this file / README if the row contract changed.

## Single writer

If multiple agents are present, the **leader commits**. Others review in chat only.

## Do not add yet

- Calibration file (wait until first 14- or 30-day closes).
- Process Health table (optional after n>=3 runs).
