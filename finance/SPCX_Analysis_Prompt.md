# SPCX Daily Analysis Prompt

**Version:** 1.4  
**Last edited:** 2026-09-01T16:30:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **SPCX** (Nasdaq: Space Exploration Technologies) with **numeric range bands** (not point targets only) that can be graded later.

- **Hit** = regular-session (or horizon-window) H/L/Close stayed inside the **range**, not only the bias.
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.
- **1d window = the next regular session after `analysis_date`.** The Analysis job runs mid-session (~11:00 ET); do not grade 1d on leftover same-day minutes. 1w/1m/3m path starts at analysis as-of (includes the remainder of the analysis-date session + subsequent sessions).

## Process rules (always apply)

1. **ATR-proxy** — compute both (a) median true range of last 5 completed regular sessions and (b) published 14d ATR (Barchart acceptable). State both dollar values. **Range construction uses the larger** of the two when they differ by more than 20%. Do not blend down to a mid-point that shrinks 1d/1w width after a quiet week while 14d ATR is still elevated.
2. **Regime:** `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - Do **not** label digestion the day after a Rel Vol >= 1.0x trend-up close (close in the top third of the session range).
   - Rel Vol used for regime is the **last completed** regular session vs 20d average volume. Mid-session volume is incomplete — do not classify trend-up from an in-progress print.
3. **Range construction**
   - **1-day is mandatory** and maps to the **next regular session**. Width >= **2.0 × ATR-proxy**. Trend-up never centered below last completed close.
   - 1-week width >= **3.0 × ATR-proxy**; if trend-up, upside leg from last completed close >= 1.5× downside leg.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` >= `max(last completed close, analysis-date session high already printed)` + **0.5 × ATR-proxy**. Never park the 1d/1w high on a wick or round magnet.
   - **Spike-fade:** if (session high − last/close) >= 0.8 × ATR, do not treat that wick high as a hard cap; still apply the 0.5× ATR clearance.
4. **Volume / confidence**
   - `pred_rel_vol` = last **completed** session volume vs 20d avg, bucketed `below-avg` | `normal` | `elevated`. Use the **same** value on all four rows for that `analysis_date`.
   - `prior_day_pct` = last **completed** regular session % change (not the in-progress session). Compute from official RTH close vs prior official RTH close.
   - If last completed Rel Vol < 0.5x: cut 1d upside-bias confidence **10 points** and do not treat a coil as a confirmed breakout.
5. Mid-session labels: price is **Last** (not Close). Rel Vol for the in-progress session is **incomplete**. Confidence <= 80 until a completed close is used as the as-of.
6. Include **prior-scenario vs actual** from the tracker when closed rows exist. If none exist, write `prior-scenario: no closed tracker rows yet`.
7. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit (or `no closed 1w yet`).
8. **Parseable table first (v1.4):** immediately after Key Takeaway (before snapshot/narrative), output the 4-row table matching tracker columns: horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct. Notification emails truncate; Auditor recovery depends on this table being in the first screenful.
9. **Self-check** (one line): `1d width $X vs ATR-proxy $Y (last-5 med $A / 14d $B; used larger: yes/no); 1d maps to next session YYYY-MM-DD; last completed Rel Vol Z.Zx; 1d high $C vs last session high $D; pred_rel_vol same on all 4 rows (yes/no); TRACKER_SHA present (yes/no).`
10. **Non-session days (weekend / US market holiday):** If `analysis_date` has **no Nasdaq regular session**, do **not** append new `(analysis_date, horizon)` rows. Friday's (or last session's) 1d already maps to the next RTH — a Saturday/Sunday 1d is a duplicate window. First line: `session: closed (weekend/holiday YYYY-MM-DD); no new rows`. Still **update path actuals** (H/L/C) on existing open 1w/1m/3m rows using the last completed **official RTH** OHLC (SpaceX IR or Yahoo) if those actuals are stale or mid-session only. Do not change ranges on already-open rows.
11. **Horizon close windows (Auditor grades; Analysis may annotate notes):**
    - **1d** closes after the mapped next regular session's official RTH close.
    - **1w** closes after the **5th regular session that begins after `analysis_date`** (next 5 RTH days). Do not close a mid-week 1w on that week's Friday just because the calendar week ended.
    - **1m** closes after the **21st** such session; **3m** after the **63rd**.
    - Weekend/holiday `analysis_date`: subsequent sessions start at the next RTH (same 1w clock as Friday's 1w if both exist).
    - Pre-existing weekend 1d rows written before rule 10: **keep and grade** vs the same next RTH as Friday's 1d. Do not delete or expire as duplicates.
    - When updating path actuals, Analysis may tag 1w notes `Day N/5; closes after YYYY-MM-DD`.
12. **pct_error format:** `X.X%` (include the percent sign). Compute `|close − bias midpoint| / bias midpoint` when a bias band exists.
13. **Official RTH source order:** SpaceX IR, else Yahoo, else StockAnalysis / MarketWatch / Barchart. State which source. 14d ATR from Barchart is acceptable as the published ATR-proxy.
14. **Session-day path maintenance:** On a session day, after appending today's four rows, also refresh already-open multi-day rows:
    - Path `actual_low` = min low from analysis as-of through the latest print; `actual_high` = max high; `actual_close` = official RTH close if complete, else **Last**.
    - Refresh every open 1w note to `Day N/5; closes after YYYY-MM-DD` (N = regular sessions that have **begun** after that row's `analysis_date`, including an in-progress session).
    - If a prior 1d row maps to the **current** session and RTH has not closed, set status=`preliminary` and fill intra-day H/L/Last. Leave hit / directional / pct_error blank until official RTH close.
    - Do **not** change ranges, bias, conf, `pred_regime`, `pred_rel_vol`, or `prior_day_pct` on existing rows.
15. **Write-first / TRACKER_SHA gate (v1.4 — hard).** After the parseable table is composed, the FIRST tool calls must be GitHub get_file_contents on `finance/SPCX_Prediction_Tracker.md` then create_or_update_file for today's 4 rows + rule-14 path refresh. Do not write snapshot/narrative until the response contains the new tracker blob SHA. First user-visible line after the table: `TRACKER_SHA: <blob sha>`. A run that emails a report but writes 0 rows is a failed run (**2026-09-01**). If the write tool errors or the SHA is unchanged after one retry: paste the 4 markdown rows and write `WRITE FAILED` as the next heading, then stop. Auditor recovery does not convert a failed Analysis write into a pass.

## Report structure

**Key Takeaway** (one sentence)

**Parseable table** (rule 8 — 4 rows, immediately here)

`TRACKER_SHA: <blob sha>` (rule 15 — required before section 1)

1. **Current Market Snapshot** — Last/Close, change %, day's range, volume vs 20d avg, mkt cap, 1d/5d/1m performance. Label Last vs Close.
2. **Technical Analysis** — support/resistance, MAs, RSI, ATR-proxy (both last-5 and 14d), **regime**, short-term outlook.
3. **Fundamental & News** — Starlink, Starship, contracts, lock-ups, regulatory, xAI/Tesla cross-news; each catalyst with probability + timing.
4. **Forward Scenarios** (numeric bands required)
   - 1-day / **next session YYYY-MM-DD**: `$low–$high` (bias; conf %)
   - 1-week: `$low–$high` (bias; conf %)
   - 1-month: `$low–$high` (bias; conf %)
   - 3-month: `$low–$high` (bias; conf %)
   - Key invalidation
   - Prior scenarios vs actual
   - Self-check (rule 9)
5. **Decision map** (3 bullets)
6. **Risks & Disclaimer** — not financial advice

On a non-session day (rule 10), skip new bands; still state official last RTH OHLC and any path-actual updates. Path-actual write still requires `TRACKER_SHA`.

## GitHub write (mandatory — hard gate)

Get SHA of `finance/SPCX_Prediction_Tracker.md` immediately before write; retry once on conflict.

- **Session day:** Append **one row per (analysis_date, horizon)** for {1d, 1w, 1m, 3m}. Status = `open`.
- Fill `pred_regime`, `pred_rel_vol`, `prior_day_pct` on every row. `pred_rel_vol` must be identical on all four rows. 1d notes must name the next session date. 1w notes should include `Day 0/5; closes after YYYY-MM-DD`.
- **Then apply rule 14:** update path actuals + `Day N/5` on already-open 1w/1m/3m; mark mapped-today prior 1d rows `preliminary` with intra-day H/L/Last.
- **Non-session day:** Do not append rows. Update stale path actuals on open 1w/1m/3m only. Refresh `Day N/5` on open 1w notes when a session has elapsed.
- Do not duplicate existing (analysis_date, horizon) pairs.
- Do not change ranges on already-open rows from prior days.
- Do not invent backfill for missing prior dates; Auditor recovers those from task output.
- Do not overwrite `pred_regime`, `pred_rel_vol`, or `prior_day_pct` on existing rows.
- **Post-write verify:** re-get the tracker and confirm today's four `(analysis_date, horizon)` rows exist (session day) or that path actuals changed (non-session day). If absent after one retry, paste the rows and write `WRITE FAILED`.
- **Response must include the new tracker blob SHA** on its own line as `TRACKER_SHA: <sha>`. If the write fails after one retry, paste the 4 rows (or the path-actual edits) and the SHA you needed — do not mark the run successful without the write.

Cite sources. Be objective and data-driven.
