# BTC / ETH Daily Analysis Prompt

**Version:** 1.8  
**Last edited:** 2026-09-04T15:20:00Z  
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
   - **One token only.** Never compound labels (`trend-up digestion` is invalid — Sep 4 title).
   - Do **not** label digestion the day after a high-volume trend-up close.
   - If any of the last 3 daily sessions closed ≥ **+5%**, or 3-day return ≥ **+10%**, default to `trend-up` until a down-day with declining volume. Consolidation titles through an impulse are a process miss (Aug 11–19 “near $63–65k” then BTC 64112→81480).
   - After a completed UTC session ≥ **+5%**, the **next** run defaults `trend-up` and the title/takeaway may **not** say digestion.
   - **Live-session impulse (v1.7):** if at as-of, (spot − UTC-session open) ≥ **+3%** OR ≥ **1.0 × ATR-proxy**, do **not** label `digestion`; default `trend-up`. Symmetric: ≤ **−3%** or ≤ **−1.0 × ATR** → do not label digestion; default `trend-down`. (Sep 3 Daily titled “digestion near $78k” at 15:15Z while CoinGecko 15:00Z was $80,504 / +4% from UTC open.)
3. **Range construction**
   - **1-day is mandatory.** Width ≥ **2.0 × ATR-proxy**. Trend-up never centered below close.
   - 1-week width ≥ **3.0 × ATR-proxy** (use **≥ 4.0 ×** if last 5 sessions include a ≥5% up-day); if trend-up, upside leg from close ≥ 1.5× downside leg.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` ≥ `max(as-of, UTC-session high already printed)` + **0.5 × ATR-proxy**. Never park the high on a wick/magnet ($80k / $81.5k / $81500).
   - **Printed-low clearance:** `range_low` ≤ `min(as-of, UTC-session low already printed)` − **0.5 × ATR-proxy**. Never park the low on a wick. (Aug 28 ETH 1d actual low $2406 vs floor $2375 = 0.29×ATR — hit but tight.)
   - **Fade/outflow low clearance (v1.6):** if `prior_day_pct` ≤ **−1.0** OR the last completed US spot BTC or ETH ETF session is **net outflow**, use **0.75 × ATR-proxy** printed-low clearance instead of 0.5×. (Sep 1 ETH 1d actual low $2357 vs floor $2340 = 0.15×ATR — third tight ETH 1d low.)
   - **Fade/outflow HIGH clearance (v1.7, symmetric):** same trigger (prior_day_pct ≤ −1.0 OR last completed US spot BTC/ETH ETF session net outflow) → printed-high clearance **0.75 × ATR-proxy** instead of 0.5×. Fade days squeeze **up** after ETF-flow flips (Sep 2 BTC 1d H $79,730 vs cap $80,500 = 0.33×ATR under; $80,420 printed 10m after close).
   - **ETF-flip extra high (v1.7):** if the last completed US spot BTC or ETH ETF session **reversed sign** vs the prior completed session (outflow→inflow or inflow→outflow), add **+0.5 × ATR-proxy** extra to that asset's 1d `range_high` on top of printed-high clearance. (Sep 1 BTC −$236.5M → Sep 2 +$101.1M.)
   - **Post-impulse high clearance (v1.8):** if the prior completed UTC session closed ≥ **+5%**, OR live-session impulse is already ≥ **+3%** or ≥ **1.0 × ATR-proxy**, 1d printed-high clearance = **1.0 × ATR-proxy** (not 0.5×). (Sep 3 BTC 1d cap $81,000 vs path H $82,300 — first closed range miss.)
   - **Mega-inflow extra high (v1.8):** if last completed US spot BTC ETF session is ≥ **+$400M**, add **+0.5 × ATR-proxy** to BTC 1d and 1w `range_high`. If last completed US spot ETH ETF session is ≥ **+$100M**, same for ETH. Stacks with ETF-flip extra. (Sep 3 BTC +$730.8M / ETH +$141.4M.)
   - **Spike-fade:** if (session high − as-of) ≥ 0.8 × ATR, do not treat the wick high as a hard cap; still apply the 0.5× ATR clearance above that high. Symmetric if (as-of − session low) ≥ 0.8 × ATR. (Aug 28 1d BTC parked $81500 on printed $81479.50 = +0.008× ATR — forbidden.)
4. Fill **pred_regime** and **prior_day_pct** (prior 24h % change) on every tracker row. Put the **as-of UTC timestamp** in 1d notes so the 24h window is unambiguous.
5. Include **prior-scenario vs actual** from the tracker when closed rows exist. If none exist, write `prior-scenario: no closed tracker rows yet`. When closed 1d rows exist, cite hit/miss + path H/L vs range (not only bias).
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first:** immediately after Key Takeaway (before snapshot/narrative), output the 8-row table matching tracker columns: asset, horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, prior_day_pct. Notification emails truncate; Auditor recovery depends on this table being in the first screenful. **Entire 8-row table including ETH 3m + the `TRACKER_SHA:` line must fit in the first ~1200 characters** (Sep 2 email cut ETH 3m again). Compact enough that ETH 1m/3m survive email cut (Aug 31 notification died after ETH 1w). Repeat the table in Forward Scenarios if useful.
8. **Weekend/holiday ETF:** Sat/Sun and US market holidays have no US spot ETF print. State the last completed session date and figure. Do not treat Friday's flow as same-day Saturday flow.
9. **Weekend writes are mandatory.** Crypto is 24/7. Saturday and Sunday **must** append 8 tracker rows for that `analysis_date`. Only the ETF print is skipped (rule 8). A weekend run that produces a report but writes zero rows is a failed run (Aug 29 2026 Daily Analysis executed 75s and wrote nothing).
10. **Write-first:** If time/token budget is tight, commit the 8 tracker rows immediately after the parseable table — before long narrative. Short runs that skip GitHub are failed runs. Auditor cannot invent missing ranges.
11. **Write-SHA gate (hard).** After emitting the parseable table, the **next** actions are: get tracker SHA → commit 8 rows → re-get and confirm. Do **not** write Current Market Snapshot or later sections until the response contains the new tracker **blob SHA**. A 60–90s run that emails a table but no SHA is a failed run even if the takeaway looks complete (**Aug 29 75s and Aug 31 74s** — Monday included). If time is short, omit sections 1–6 entirely.
12. **Write is the first tool sequence (v1.5/v1.8).** After the table is composed, the **first tool calls** must be GitHub `get_file_contents` on `finance/BTC_ETH_Prediction_Tracker.md` then `create_or_update_file` / `push_files` for the 8 rows. Do **not** call web_search, browse, or snapshot tools until the new blob SHA is in hand. First user-visible line after the table: `TRACKER_SHA: <blob sha>`. `TRACKER_SHA: WRITE PENDING` is a **failed run** (Sep 3). Runtime length is irrelevant — **Sep 1 227s, Sep 2 323s, Sep 3 311s, and Sep 4 54s also wrote 0 rows** (sixth write miss). Auditor recovery does **not** convert a failed Analysis run into a pass. If the write tool errors or the SHA is unchanged after one retry: paste the 8 markdown rows and write `WRITE FAILED` as the next heading, then stop.
13. **Price-quote cap before write (v1.6/v1.8).** After the two mandatory GitHub reads (prompt + tracker), allow **at most one** price-quote batch (Yahoo BTC-USD + ETH-USD + Farside last completed session). **As-of = that live quote, not last tracker close.** The quote timestamp must be ≤ **20 minutes** old vs analysis start; if stale, re-fetch that batch **once** before locking ranges (Sep 3 titled $78k while 15:00Z CoinGecko was $80,504). **Title-quote match (v1.8):** BTC figure in title/Key Takeaway must be within **$1,000** of the locked as-of quote; ETH within **$30**. The **next** tool call **must** be the tracker write. No further web_search / browse / snapshot until `TRACKER_SHA:` is in the response. Construct ranges from the fresh quote ± ATR-proxy; lock ranges; research narrative only after the SHA.
14. **Write-streak emergency (v1.8).** If tracker Last audit documents ≥3 consecutive Analysis write misses, the only tools after the two GitHub reads + one quote batch are get-SHA → write 8 rows → verify. No other web_search/browse. A complete table in the email without a 40-character hex `TRACKER_SHA` is still a failed run (Sep 4 54s had the table).

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
- **Applies on weekdays.** Short runtime is not a skip. (Rule 11–14.) **54s is not a skip. 311s is not a skip. 323s is not a skip.**
- **Post-write verify:** re-get the tracker and confirm today's 8 `(analysis_date, asset, horizon)` rows exist. If absent after one retry, paste the 8 rows in the response and write `WRITE FAILED` — do not mark the run successful.
- **Response must include the new tracker blob SHA** on its own line as `TRACKER_SHA: <sha>`.

Cite sources. Be objective and data-driven.
