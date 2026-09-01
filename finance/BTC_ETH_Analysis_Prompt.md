# BTC / ETH Daily Analysis Prompt

**Version:** 1.5  
**Last edited:** 2026-09-01T15:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** BTC ETH Daily Crypto Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **BTC and ETH** with **numeric range bands** (not point targets only) that can be graded later:

- Hit = path high/low **and** as-of close stayed inside the **range** over the horizon window (crypto is 24/7; **1d = 24h from as-of**, not NYSE close).
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.

## Process rules (always apply)

1. **ATR-proxy** — median true range of last 5 daily sessions (or published 14d ATR). State dollar value for BTC and ETH.
2. **Regime** per asset: `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - Do **not** label digestion the day after a high-volume trend-up close.
   - If any of the last 3 daily sessions closed ≥ **+5%**, or 3-day return ≥ **+10%**, default to `trend-up` until a down-day with declining volume. Consolidation titles through an impulse are a process miss (Aug 11–19 “near $63–65k” then BTC 64112→81480).
3. **Range construction**
   - **1-day is mandatory.** Width ≥ **2.0 × ATR-proxy**. Trend-up never centered below close.
   - 1-week width ≥ **3.0 × ATR-proxy** (use **≥ 4.0 ×** if last 5 sessions include a ≥5% up-day); if trend-up, upside leg from close ≥ 1.5× downside leg.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` ≥ `max(as-of, UTC-session high already printed)` + **0.5 × ATR-proxy**. Never park the high on a wick/magnet.
   - **Printed-low clearance:** `range_low` ≤ `min(as-of, UTC-session low already printed)` − **0.5 × ATR-proxy**. Never park the low on a wick. (Aug 28 ETH 1d actual low $2406 vs floor $2375 = 0.29×ATR — hit but tight.)
   - **Spike-fade:** if (session high − as-of) ≥ 0.8 × ATR, do not treat the wick high as a hard cap; still apply the 0.5× ATR clearance above that high. Symmetric if (as-of − session low) ≥ 0.8 × ATR. (Aug 28 1d BTC parked $81500 on printed $81479.50 = +0.008× ATR — forbidden.)
4. Fill **pred_regime** and **prior_day_pct** (prior 24h % change) on every tracker row. Put the **as-of UTC timestamp** in 1d notes so the 24h window is unambiguous.
5. Include **prior-scenario vs actual** from the tracker when closed rows exist. If none exist, write `prior-scenario: no closed tracker rows yet`. When closed 1d rows exist, cite hit/miss + path H/L vs range (not only bias).
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first:** immediately after Key Takeaway (before snapshot/narrative), output the 8-row table matching tracker columns: asset, horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, prior_day_pct. Notification emails truncate; Auditor recovery depends on this table being in the first screenful. Compact enough that ETH 1m/3m survive email cut (Aug 31 notification died after ETH 1w). Repeat the table in Forward Scenarios if useful.
8. **Weekend/holiday ETF:** Sat/Sun and US market holidays have no US spot ETF print. State the last completed session date and figure. Do not treat Friday's flow as same-day Saturday flow.
9. **Weekend writes are mandatory.** Crypto is 24/7. Saturday and Sunday **must** append 8 tracker rows for that `analysis_date`. Only the ETF print is skipped (rule 8). A weekend run that produces a report but writes zero rows is a failed run (Aug 29 2026 Daily Analysis executed 75s and wrote nothing).
10. **Write-first:** If time/token budget is tight, commit the 8 tracker rows immediately after the parseable table — before long narrative. Short runs that skip GitHub are failed runs. Auditor cannot invent missing ranges.
11. **Write-SHA gate (hard).** After emitting the parseable table, the **next** actions are: get tracker SHA → commit 8 rows → re-get and confirm. Do **not** write Current Market Snapshot or later sections until the response contains the new tracker **blob SHA**. A 60–90s run that emails a table but no SHA is a failed run even if the takeaway looks complete (**Aug 29 75s and Aug 31 74s** — Monday included). If time is short, omit sections 1–6 entirely.
12. **Write is the first tool sequence (v1.5).** After the table is composed, the **first tool calls** must be GitHub `get_file_contents` on `finance/BTC_ETH_Prediction_Tracker.md` then `create_or_update_file` / `push_files` for the 8 rows. Do **not** call web_search, browse, or snapshot tools until the new blob SHA is in hand. First user-visible line after the table: `TRACKER_SHA: <blob sha>`. Runtime length is irrelevant — **Sep 1 227s also wrote 0 rows**. Auditor recovery does **not** convert a failed Analysis run into a pass. If the write tool errors or the SHA is unchanged after one retry: paste the 8 markdown rows and write `WRITE FAILED` as the next heading, then stop.

## Report structure

**Key Takeaway** (one sentence)

**Parseable table** (rule 7 — 8 rows, immediately here)

`TRACKER_SHA: <blob sha>` (rule 12 — required before section 1)

1. **Current Market Snapshot** — prices, 24h %, volume, mkt caps; 1d / 7d / 30d performance for BTC and ETH.
2. **Technical Analysis** — support/resistance, MAs, RSI, ATR-proxy, **regime**, short-term outlook (1–3d and 1w) with probability ranges.
3. **Fundamental & News** — ETF flows (with session date), institutional, regulatory, macro, on-chain; catalysts with probability + timing.
4. **Forward Scenarios** (numeric bands required)
   - BTC: **1d** / 1w / 1m / 3m — `$low–$high` (bias low–high; conf %)
   - ETH: same
   - Correlation note; overall crypto outlook; confidence low/medium/high
   - Key invalidation levels
   - Prior scenarios vs actual (from tracker)
5. **Decision map** (3 bullets)
6. **Risks & Disclaimer** — top 3 risks + upside catalysts; not financial advice.

## GitHub write (mandatory — hard gate)

Get SHA of `finance/BTC_ETH_Prediction_Tracker.md` immediately before write; retry once on conflict.

- Append **one row per (analysis_date, asset, horizon)** for BTC and ETH × **{1d, 1w, 1m, 3m}**. Status = `open`.
- Columns: analysis_date, asset, horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, prior_day_pct, (actuals blank), hit blank, directional blank, pct_error blank, status=open, notes.
- Do not duplicate existing (analysis_date, asset, horizon) pairs.
- Do not change ranges on already-open rows from prior days.
- Do not invent backfill for missing prior dates; Auditor recovers those from task output.
- **Applies on Sat/Sun.** Do not treat weekend as a skip. (Rule 9.)
- **Applies on weekdays.** Short runtime is not a skip. (Rule 11–12.) **227s is not a skip.**
- **Post-write verify:** re-get the tracker and confirm today's 8 `(analysis_date, asset, horizon)` rows exist. If absent after one retry, paste the 8 rows in the response and write `WRITE FAILED` — do not mark the run successful.
- **Response must include the new tracker blob SHA** on its own line as `TRACKER_SHA: <sha>`.

Cite sources. Be objective and data-driven.
