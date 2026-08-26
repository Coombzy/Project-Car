# BTC / ETH Daily Analysis Prompt

**Version:** 1.0  
**Last edited:** 2026-08-26T23:30:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** BTC ETH Daily Crypto Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **BTC and ETH** with **numeric range bands** (not point targets only) that can be graded later:

- Hit = path high/low **and** as-of close stayed inside the **range** over the horizon window (crypto is 24/7).
- Horizons: 1-day (optional), 1-week, 1-month, 3-month.

## Process rules (always apply)

1. **ATR-proxy** — median true range of last 5 daily sessions (or published 14d ATR). State dollar value for BTC and ETH.
2. **Regime** per asset: `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - Do **not** label digestion the day after a high-volume trend-up close.
3. **Range construction**
   - 1-week width ≥ **3.0 × ATR-proxy**; if trend-up, upside leg from close ≥ 1.5× downside leg.
   - 1-day (if included) width ≥ **2.0 × ATR-proxy**; trend-up never centered below close.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
4. Fill **pred_regime** and **prior_day_pct** (prior 24h % change) on every tracker row.
5. Include **prior-scenario vs actual** from the tracker when closed rows exist.
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.

## Report structure

**Key Takeaway** (one sentence)

1. **Current Market Snapshot** — prices, 24h %, volume, mkt caps; 1d / 7d / 30d performance for BTC and ETH.
2. **Technical Analysis** — support/resistance, MAs, RSI, ATR-proxy, **regime**, short-term outlook (1–3d and 1w) with probability ranges.
3. **Fundamental & News** — ETF flows, institutional, regulatory, macro, on-chain; catalysts with probability + timing.
4. **Forward Scenarios** (numeric bands required)
   - BTC: 1w / 1m / 3m (and 1d if used) — `$low–$high` (bias low–high; conf %)
   - ETH: same
   - Correlation note; overall crypto outlook; confidence low/medium/high
   - Key invalidation levels
   - Prior scenarios vs actual (from tracker)
5. **Decision map** (3 bullets)
6. **Risks & Disclaimer** — top 3 risks + upside catalysts; not financial advice.

## GitHub write (mandatory)

Get SHA of `finance/BTC_ETH_Prediction_Tracker.md` immediately before write; retry once on conflict.

- Remove the seed placeholder row on the first real write.
- Append **one row per (analysis_date, asset, horizon)** for BTC and ETH × {1w, 1m, 3m} (and 1d if produced). Status = `open`.
- Columns: analysis_date, asset, horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, prior_day_pct, (actuals blank), hit blank, directional blank, pct_error blank, status=open, notes.
- Do not duplicate existing (analysis_date, asset, horizon) pairs.
- Do not change ranges on already-open rows from prior days.

Cite sources. Be objective and data-driven.
