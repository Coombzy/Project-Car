# BTC / ETH Daily Analysis Prompt

**Version:** 1.24  
**Last edited:** 2026-09-19T15:25:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** BTC ETH Daily Crypto Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **BTC and ETH** with **numeric range bands** (not point targets only) that can be graded later:

- Hit = path high/low **and** as-of close stayed inside the **range** over the horizon window (crypto is 24/7; **1d = 24h from as-of**, not NYSE close).
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.

## Process rules (always apply)

1. **ATR-proxy (v1.17)** — median true range of last 5 **completed weekday** UTC sessions. Exclude Sat/Sun and US-holiday thin sessions. Or published 14d ATR. State dollar value for BTC and ETH. (Recalc each run from THIS-RUN weekday-5 TR list — never reuse $2100 / $3200 / any prior example. 14/15/16/17/18 Sep BTC TRs ~3202/3298/1478/1133/5104 median ~$3200; ETH TRs ~147/161/58/69/184 median ~$147. Sep 17 Daily reused stale $2100 → 1d width $4800 < 2.0×$3200=$6400 and cap $78700 vs path H $81332.)
2. **Regime** per asset: `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - **One token only.** Never compound labels (`trend-up digestion` is invalid — Sep 4 title).
   - Do **not** label digestion the day after a high-volume trend-up close.
   - If any of the last 3 daily sessions closed ≥ **+5%**, or 3-day return ≥ **+10%**, default to `trend-up` until a down-day with declining volume.
   - After a completed UTC session ≥ **+5%**, the **next** run defaults `trend-up` and the title/takeaway may **not** say digestion.
   - **Takeaway word-ban (v1.9):** if `pred_regime` is `trend-up`, the Key Takeaway and title must **not** contain the word `digestion`.
   - **Live-session impulse (v1.7):** if at as-of, (spot − UTC-session open) ≥ **+3%** OR ≥ **1.0 × ATR-proxy**, do **not** label `digestion`; default `trend-up`. Symmetric down.
   - **Two-down bounce (v1.13):** if the last **two completed** UTC sessions are both down, do **not** flip to `trend-up` on a sub-1.0×ATR bounce. Stay `digestion` (or `failed-break` if a break failed) unless live impulse ≥ **+3%** / **1.0 × ATR** **or** last completed close reclaimed the prior swing high.
   - **Beta-divergence (v1.15):** if |ETH live% − BTC live%| ≥ **4pp**, the leader is **not** `digestion` and gets +**0.5 × ATR** extra 1d high. (Sep 11 ETH ~+7% vs BTC ~+2% labeled digestion.)
3. **Range construction**
   - **1-day is mandatory.** Width ≥ **2.0 × ATR-proxy**. Trend-up never centered below close.
   - 1-week width ≥ **3.0 × ATR-proxy** (≥ **4.0 ×** if last 5 weekday sessions include a ≥5% up-day); if trend-up, upside leg from close ≥ 1.5× downside leg.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` ≥ `max(as-of, UTC-session high already printed)` + **0.5 × ATR-proxy**. Never park the high on a wick/magnet ($80k / $81.5k / $81500).
   - **Printed-low clearance:** `range_low` ≤ `min(as-of, UTC-session low already printed)` − **0.5 × ATR-proxy**.
   - **Weekend printed-extreme carry-forward (v1.16):** Sat/Sun and US holidays use the **last completed UTC session** high/low as the printed extreme, not today's thin weekend session. `range_high` ≥ last-completed-UTC high + applicable clearance; `range_low` ≤ last-completed-UTC low − applicable clearance.
   - **Fade/outflow low+high clearance (v1.6/v1.7):** if `prior_day_pct` ≤ **−1.0** OR last completed US spot ETF **for that asset** is net outflow, use **0.75 × ATR-proxy** printed-low AND printed-high clearance.
   - **Post-fade stacked low (v1.14):** if the last **completed** UTC session is down **AND** last completed US spot ETF for that asset is net outflow, 1d printed-low clearance = **1.0 × ATR-proxy**. Stacks over 0.75× fade — use the larger clearance.
   - **ETF-flip extra high (v1.7):** last completed US spot BTC or ETH ETF session reversed sign vs prior session → +**0.5 × ATR-proxy** extra to that asset's 1d `range_high`.
   - **Post-impulse high clearance (v1.8):** prior completed UTC session ≥ **+5%** OR live impulse ≥ **+3%** / **1.0 × ATR** → 1d printed-high clearance = **1.0 × ATR-proxy**. (Sep 3 BTC 1d cap $81,000 vs path H $82,300.)
   - **Live-impulse low clearance (v1.20):** if at as-of, (UTC-session open − spot) ≥ **3%** OR ≥ **1.0 × ATR-proxy**, 1d printed-low clearance = **1.0 × ATR-proxy**.
   - **Mega-inflow extra high (v1.8):** last completed US spot BTC ETF ≥ **+$400M** → +0.5×ATR to BTC 1d and 1w high. ETH ETF ≥ **+$100M** → same for ETH. Stacks. Last completed **18 Sep** BTC +$433.0M / ETH +$143.7M.
   - **Known-macro extra high (v1.19):** CPI/PCE/FOMC/NFP extra applies only if the **event timestamp** is ≤ as-of+24h.
   - **Post-event lag-squeeze high (v1.23):** if FOMC/CPI/PCE/NFP timestamp is in the prior 24h (already printed), 1d printed-high clearance = **1.0×ATR** even when pred_regime is digestion. Also 1d range_high ≥ as-of + **1.5×ATR**. Stacks — use the larger. Sep 17 Daily cap $78700 vs path H $81332 after FOMC 16 Sep 18:00Z.
   - **Spike-fade:** wick ≥ 0.8×ATR is not a cap; still apply 0.5×ATR clearance above that high.
   - **RANGE_CHECK (v1.17/v1.20/v1.23 — hard).** Print this-run weekday-5 TR list + median + post-event-high 1.0x yes/no + live-impulse-low 1.0x yes/no for BTC and ETH. If 1d width < 2.0×ATR or high/low miss required clearance, widen and reprint before writing. Never reuse a dollar ATR from a prior run or this prompt example.
4. Fill **pred_regime** and **prior_day_pct** on every tracker row. **conf** integer **40–85**. **prior_day_pct** = Yahoo BTC-USD / ETH-USD official UTC Close pair only. Print `source: Yahoo YYYY-MM-DD $c1 → YYYY-MM-DD $c2 = Z%`.
5. Include **prior-scenario vs actual** from the tracker when closed rows exist.
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first:** immediately after Key Takeaway, 8-row table. Entire table + `RANGE_CHECK:` + `TRACKER_SHA:` in first ~1400 characters.
8. **Weekend/holiday ETF:** **Last completed as of 2026-09-19 = Thu 2026-09-18 BTC +$433.0M / ETH +$143.7M (mega-inflow both).** 17 Sep BTC +$159.5M / ETH −$39.3M. 16 Sep BTC −$295.9M / ETH −$224.1M. 15 Sep BTC −$450.4M / ETH −$142.3M. Sat 19 Sep Farside 0.0 is not a completed print.
9. **Weekend writes are mandatory** only if today's 8 rows do not already exist.
10. **Write-first.** `WRITE PENDING` banned.
11. **Write-SHA gate (hard).** Emitted SHA must differ from pre-write SHA.
12. **push_files-first** full merged body. create_or_update_file is fallback after a ≥100-row SHA.
13. **Price-quote cap.** One Yahoo BTC+ETH history Close + live Last + Farside batch.
14. **Write-streak emergency ON.** Sub-90s no new SHA = WRITE FAILED.
    - **Truncation fallback (v1.19).** get_file_contents truncates ~20kB. Fetch raw.githubusercontent if body ends mid-row.
    - **Inbound-floor (v1.21).** ≥100 data rows and ≥15kB before any non-restore write. Restore = f2d4bf74 / c0c37a51.
    - **Preexisting-rows skip.** If today's 8 exist, emit PREEXISTING_ROWS + current SHA.
    - **Outbound-row-count (v1.18).** Pushed body MUST contain ≥ inbound count AND ≥100 rows.
    - **POST-WRITE VERIFY (v1.22/v1.24).** Fetch raw main tracker. If rows <100 OR size <15kB OR PLACEHOLDER / header-only / 8-row stub, do NOT emit TRACKER_SHA. Immediately restore-merge f2d4bf74/c0c37a51 + today's 8. Stubs e22b9936 / 0e4d529a / ae5f666d / 469ebcc7 are WRITE FAILED.
15. **Append-only / anti-wipe (hard).** Never write PLACEHOLDER / SEE_LOCAL_FULL_FILE / SEE_FILE / header-only to tracker **or this prompt**. After writing this prompt, raw size must be ≥8kB. Restore source f2d4bf74 / c0c37a51. Fallback 41e4ad58 / 47d11800.
16. **Role split.** Daily inserts new analysis_date rows only. Auditor grades/path-refreshes/closes only. Auditor may recover a Daily block Daily already attempted and wiped.
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
