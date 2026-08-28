# SPCX Daily Analysis Prompt

**Version:** 1.0  
**Last edited:** 2026-08-28T16:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **SPCX** (Nasdaq: Space Exploration Technologies) with **numeric range bands** (not point targets only) that can be graded later.

- **Hit** = regular-session (or horizon-window) H/L/Close stayed inside the **range**, not only the bias.
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.
- **1d window = the next regular session after `analysis_date`.** The Analysis job runs mid-session (~11:00 ET); do not grade 1d on leftover same-day minutes. 1w/1m/3m path starts at analysis as-of (includes the remainder of the analysis-date session + subsequent sessions).

## Process rules (always apply)

1. **ATR-proxy** — median true range of last 5 completed regular sessions, and/or published 14d ATR. State the dollar value and which definition was used.
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
   - `prior_day_pct` = last **completed** regular session % change (not the in-progress session).
   - If last completed Rel Vol < 0.5x: cut 1d upside-bias confidence **10 points** and do not treat a coil as a confirmed breakout.
5. Mid-session labels: price is **Last** (not Close). Rel Vol for the in-progress session is **incomplete**. Confidence <= 80 until a completed close is used as the as-of.
6. Include **prior-scenario vs actual** from the tracker when closed rows exist. If none exist, write `prior-scenario: no closed tracker rows yet`.
7. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit (or `no closed 1w yet`).
8. **Parseable table** in Forward Scenarios matching tracker columns: horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct.
9. **Self-check** (one line): `1d width $X vs ATR-proxy $Y; 1d maps to next session YYYY-MM-DD; last completed Rel Vol Z.Zx; 1d high $A vs last session high $B.`

## Report structure

**Key Takeaway** (one sentence)

1. **Current Market Snapshot** — Last/Close, change %, day's range, volume vs 20d avg, mkt cap, 1d/5d/1m performance. Label Last vs Close.
2. **Technical Analysis** — support/resistance, MAs, RSI, ATR-proxy, **regime**, short-term outlook.
3. **Fundamental & News** — Starlink, Starship, contracts, lock-ups, regulatory, xAI/Tesla cross-news; each catalyst with probability + timing.
4. **Forward Scenarios** (numeric bands required)
   - 1-day / **next session YYYY-MM-DD**: `$low–$high` (bias; conf %)
   - 1-week: `$low–$high` (bias; conf %)
   - 1-month: `$low–$high` (bias; conf %)
   - 3-month: `$low–$high` (bias; conf %)
   - Parseable table (rule 8)
   - Key invalidation
   - Prior scenarios vs actual
   - Self-check (rule 9)
5. **Decision map** (3 bullets)
6. **Risks & Disclaimer** — not financial advice

## GitHub write (mandatory — hard gate)

Get SHA of `finance/SPCX_Prediction_Tracker.md` immediately before write; retry once on conflict.

- Append **one row per (analysis_date, horizon)** for {1d, 1w, 1m, 3m}. Status = `open`.
- Fill `pred_regime`, `pred_rel_vol`, `prior_day_pct` on every row. 1d notes must name the next session date.
- Do not duplicate existing (analysis_date, horizon) pairs.
- Do not change ranges on already-open rows from prior days.
- Do not invent backfill for missing prior dates; Auditor recovers those from task output.
- **Response must include the new tracker blob SHA.** If the write fails after one retry, paste the 4 rows and the SHA you needed — do not mark the run successful without rows.

Cite sources. Be objective and data-driven.
