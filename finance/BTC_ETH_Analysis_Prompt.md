# BTC / ETH Daily Analysis Prompt

**Version:** 1.28  
**Last edited:** 2026-09-25T15:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** BTC ETH Daily Crypto Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **BTC and ETH** with **numeric range bands** (not point targets only) that can be graded later:

- Hit = path high/low **and** as-of close stayed inside the **range** over the horizon window (crypto is 24/7; **1d = 24h from as-of**, not NYSE close).
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.

## Process rules (always apply)

1. **ATR-proxy (v1.17)** — median true range of last 5 **completed weekday** UTC sessions. Exclude Sat/Sun and US-holiday thin sessions. Or published 14d ATR. State dollar value for BTC and ETH. Recalc each run from THIS-RUN weekday-5 TR list — never reuse $2100 / $3200 / $1970 / any prior example. (Sep 17 Daily reused stale $2100 → 1d width $4800 < 2.0×$3200=$6400 and cap $78700 vs path H $81332.)
2. **Regime** per asset: `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - **One token only.** Never compound labels.
   - Do **not** label digestion the day after a high-volume trend-up close.
   - If any of the last 3 daily sessions closed ≥ **+5%**, or 3-day return ≥ **+10%**, default to `trend-up` until a down-day with declining volume.
   - After a completed UTC session ≥ **+5%**, the **next** run defaults `trend-up` and the title/takeaway may **not** say digestion.
   - **Takeaway word-ban (v1.9):** if `pred_regime` is `trend-up`, the Key Takeaway and title must **not** contain the word `digestion`.
   - **Live-session impulse (v1.7):** if at as-of, (spot − UTC-session open) ≥ **+3%** OR ≥ **1.0 × ATR-proxy**, do **not** label `digestion`; default `trend-up`. Symmetric down.
   - **Two-down bounce (v1.13):** if the last **two completed** UTC sessions are both down, do **not** flip to `trend-up` on a sub-1.0×ATR bounce. Stay `digestion` (or `failed-break`) unless live impulse ≥ **+3%** / **1.0 × ATR** **or** last completed close reclaimed the prior swing high.
   - **Beta-divergence (v1.15):** if |ETH live% − BTC live%| ≥ **4pp**, the leader is **not** `digestion` and gets +**0.5 × ATR** extra 1d high.
3. **Range construction**
   - **1-day is mandatory.** Width ≥ **2.0 × ATR-proxy**. After a completed UTC ≥ **+5%**, next 1d width ≥ **2.5 × ATR-proxy**. Trend-up never centered below close.
   - 1-week width ≥ **3.0 × ATR-proxy** (≥ **4.0 ×** if last 5 weekday sessions include a ≥5% up-day); if trend-up, upside leg from close ≥ 1.5× downside leg.
   - **Post-+5% / mega-inflow / in-window 1w high (v1.28):** after a completed UTC ≥ **+5%** OR last-completed mega-inflow (BTC ETF ≥+$400M / ETH ETF ≥+$100M) OR a +5% session high still inside the open 1w window OR FOMC/CPI/PCE/NFP inside that 1w window: 1w `range_high` ≥ `max(that session high, quote-page Day Range H)` + **1.5 × ATR-proxy** even if digestion. Applies to the **next** 1w print and is the construction miss behind Sep 14/15/17 1w caps $86000 vs later path H $87364. Hard-fail reprint if 1w high is parked on $78700 / $81000 / $82000 / $85000 / $86000 / $87000 / $88000. (Sep 12 cap $82000 vs H $81911; Sep 14 cap $86000 vs H $86284; Sep 15/17 cap $86000 vs H $87364; Sep 17 1d cap $78700 vs H $81332.)
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` ≥ `max(as-of, UTC-session high already printed, quote-page Day Range H)` + **0.5 × ATR-proxy**. Never park the high on a wick/magnet ($80k / $81.5k / $81500 / $86000 / $87000).
   - **Printed-low clearance:** `range_low` ≤ `min(as-of, UTC-session low already printed, quote-page Day Range L)` − **0.5 × ATR-proxy**.
   - **Quote-page day-range (v1.26/v1.27):** RANGE_CHECK printed extremes = Yahoo quote-page Day Range H/L at as-of, **not** the history-table High. (21 Sep history-table H ~$81805 vs live Day Range H $86284 / session H $87364.)
   - **Weekend printed-extreme carry-forward (v1.16):** Sat/Sun and US holidays use the **last completed UTC session** high/low as the printed extreme. `range_high` ≥ last-completed-UTC high + applicable clearance; `range_low` ≤ last-completed-UTC low − applicable clearance.
   - **Fade/outflow low+high clearance (v1.6/v1.7):** if `prior_day_pct` ≤ **−1.0** OR last completed US spot ETF **for that asset** is net outflow, use **0.75 × ATR-proxy** printed-low AND printed-high clearance.
   - **Post-fade stacked low (v1.14):** if the last **completed** UTC session is down **AND** last completed US spot ETF for that asset is net outflow, 1d printed-low clearance = **1.0 × ATR-proxy**. Stacks — use the larger.
   - **ETF-flip extra high (v1.7):** last completed US spot BTC or ETH ETF session reversed sign vs prior session → +**0.5 × ATR-proxy** extra to that asset's 1d `range_high`.
   - **Post-impulse high clearance (v1.8):** prior completed UTC session ≥ **+5%** OR live impulse ≥ **+3%** / **1.0 × ATR** → 1d printed-high clearance = **1.0 × ATR-proxy**. (Sep 3 BTC 1d cap $81,000 vs path H $82,300.)
   - **Live-impulse low clearance (v1.20):** if at as-of, (UTC-session open − spot) ≥ **3%** OR ≥ **1.0 × ATR-proxy**, 1d printed-low clearance = **1.0 × ATR-proxy**.
   - **Mega-inflow extra high (v1.8):** last completed US spot BTC ETF ≥ **+$400M** → +0.5×ATR to BTC 1d and 1w high. ETH ETF ≥ **+$100M** → same for ETH. Stacks. Last completed **24 Sep** BTC +$190.7M / ETH +$66.1M (neither mega). 23 Sep +$346.9M / +$104.5M (ETH mega). 22 Sep +$714.7M / +$162.2M. 21 Sep +$999.0M / +$270.0M.
   - **Squeeze-continuation extra high (v1.26/v1.27):** if that asset's futures OI 24h ≥ **+8%** AND funding > 0 AND live impulse ≥ **+3%** or ≥ **1.0×ATR**, add +**0.5×ATR** to that asset's 1d AND 1w `range_high`. Stacks with mega-inflow and post-+5%.
   - **Known-macro extra high (v1.19):** CPI/PCE/FOMC/NFP extra applies only if the **event timestamp** is ≤ as-of+24h.
   - **Post-event lag-squeeze high (v1.23):** if FOMC/CPI/PCE/NFP timestamp is in the prior 24h, 1d printed-high clearance = **1.0×ATR** even when pred_regime is digestion. Also 1d range_high ≥ as-of + **1.5×ATR**. Stacks. Sep 17 Daily cap $78700 vs path H $81332 after FOMC 16 Sep 18:00Z.
   - **Spike-fade:** wick ≥ 0.8×ATR is not a cap; still apply 0.5×ATR clearance above that high.
   - **RANGE_CHECK (v1.28 — hard).** Print this-run weekday-5 TR list + median + post-event-high 1.0x yes/no + live-impulse-low 1.0x yes/no + post-+5% 2.5x-width yes/no + squeeze-continuation 0.5x yes/no + in-window-+5% 1w-high 1.5x yes/no + quote-page Day Range H/L for BTC and ETH. If 1d width < required multiple or high/low miss required clearance, widen and reprint before writing. Hard-fail reprint if post-event-high=yes AND 1d high < as-of+1.5×ATR. Hard-fail reprint if post-+5% or mega-inflow or in-window-+5% AND 1w high < sessionH+1.5×ATR or parked on $78700/$81000/$82000/$85000/$86000/$87000/$88000. Never reuse a dollar ATR from a prior run or this prompt example.
4. Fill **pred_regime** and **prior_day_pct** on every tracker row. **conf** integer **40–85**. **prior_day_pct** = Yahoo BTC-USD / ETH-USD official UTC Close pair only. Print `source: Yahoo YYYY-MM-DD $c1 → YYYY-MM-DD $c2 = Z%`.
5. Include **prior-scenario vs actual** from the tracker when closed rows exist.
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first:** immediately after Key Takeaway, 8-row table. Entire table + `RANGE_CHECK:` + `TRACKER_SHA:` in first ~1400 characters. Email/report must print all 8 numeric rows untruncated.
8. **Weekend/holiday ETF:** **Last completed as of 2026-09-25 = 24 Sep BTC +$190.7M / ETH +$66.1M (neither mega).** 23 Sep BTC +$346.9M / ETH +$104.5M (ETH mega). 22 Sep +$714.7M / +$162.2M. 21 Sep +$999.0M / +$270.0M. 18 Sep +$433.0M / +$143.7M. Unprinted Farside 0.0 (25 Sep) is **not** a completed print — use last completed weekday.
9. **Weekend writes are mandatory** only if today's 8 rows do not already exist.
10. **Write-first.** `WRITE PENDING` banned. Email is not a write.
11. **Write-SHA gate (hard).** Emitted SHA must differ from pre-write SHA.
12. **push_files-first** full merged body. create_or_update_file is fallback after a ≥100-row SHA.
13. **Price-quote cap.** One Yahoo BTC+ETH history Close + live Last + Farside batch. If a second print within 20 min differs BTC ≥$1000 or ETH ≥$30, re-quote once before lock.
14. **Write-streak emergency ON.** Sub-90s no new SHA = WRITE FAILED.
    - **Truncation fallback (v1.19).** get_file_contents truncates ~20kB. Fetch raw.githubusercontent if body ends mid-row.
    - **Inbound-floor (v1.21).** ≥100 data rows and ≥15kB before any non-restore write. Restore = f2d4bf74 / c0c37a51.
    - **Preexisting-rows skip.** If today's 8 exist, emit PREEXISTING_ROWS + current SHA.
    - **Outbound-row-count (v1.18).** Pushed body MUST contain ≥ inbound count AND ≥100 rows. If outbound < inbound or <100, do NOT call any write tool.
    - **POST-WRITE VERIFY (v1.22/v1.25).** Fetch raw main tracker. If rows <100 OR size <15kB OR PLACEHOLDER / SEE_FILE / SEE_FILE_USE_CREATE_OR_UPDATE / header-only / 8-row stub, do NOT emit TRACKER_SHA. Immediately restore-merge f2d4bf74/c0c37a51 + today's 8.
    - **Restore-blob-only (v1.25).** Never reconstruct early rows from memory. Start from raw restore blob bytes; only mutate path/grade cells and append sourced Daily rows. Main stub is not inbound.
15. **Append-only / anti-wipe (hard).** Never write PLACEHOLDER / SEE_LOCAL_FULL_FILE / SEE_FILE / SEE_FILE_USE_CREATE_OR_UPDATE / LOADING_FULL_BODY_NEXT / header-only to tracker **or this prompt**. After writing this prompt, raw size must be ≥8kB. Restore source f2d4bf74 / c0c37a51. Fallback 41e4ad58 / 47d11800.
16. **Role split.** Daily inserts new analysis_date rows only. Auditor grades/path-refreshes/closes only. Auditor may recover a Daily block Daily already attempted and wiped. Do not invent truncated ETH/Daily tables.
17. **1d actuals = window-only.** Path inside the 24h window from as-of, not multi-week path.

## Report structure

**Key Takeaway** (one sentence)

**Parseable table** (8 rows)

`RANGE_CHECK: ...`

`TRACKER_SHA: <blob sha>`

1. Current Market Snapshot
2. Technical Analysis
3. Fundamental & News — ETF flows with session date
4. Forward Scenarios — BTC/ETH 1d/1w/1m/3m
5. Decision map (3 bullets)
6. Risks & Disclaimer — not financial advice

## GitHub write (mandatory)

Get SHA immediately before write; retry once on conflict. Dual-write full merged body. SHA-delta. Anti-wipe row-count ≥100. Never emit TRACKER_SHA on an 8-row stub.

Cite sources. Be objective and data-driven.
