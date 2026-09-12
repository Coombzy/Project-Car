# BTC / ETH Daily Analysis Prompt

**Version:** 1.16  
**Last edited:** 2026-09-12T15:25:00Z  
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
   - If any of the last 3 daily sessions closed ≥ **+5%**, or 3-day return ≥ **+10%**, default to `trend-up` until a down-day with declining volume.
   - After a completed UTC session ≥ **+5%**, the **next** run defaults `trend-up` and the title/takeaway may **not** say digestion.
   - **Takeaway word-ban (v1.9):** if `pred_regime` is `trend-up`, the Key Takeaway and title must **not** contain the word `digestion`.
   - **Live-session impulse (v1.7):** if at as-of, (spot − UTC-session open) ≥ **+3%** OR ≥ **1.0 × ATR-proxy**, do **not** label `digestion`; default `trend-up`. Symmetric down.
   - **Two-down bounce (v1.13):** if the last **two completed** UTC sessions are both down, do **not** flip to `trend-up` on a sub-1.0×ATR bounce. Stay `digestion` (or `failed-break` if a break failed) unless live impulse ≥ **+3%** / **1.0 × ATR** **or** last completed close reclaimed the prior swing high.
   - **Beta-divergence (v1.15):** if |ETH live% − BTC live%| ≥ **4pp**, the leader is **not** `digestion` and gets +**0.5 × ATR** extra 1d high. (Sep 11 ETH ~+7% vs BTC ~+2% labeled digestion.)
3. **Range construction**
   - **1-day is mandatory.** Width ≥ **2.0 × ATR-proxy**. Trend-up never centered below close.
   - 1-week width ≥ **3.0 × ATR-proxy** (≥ **4.0 ×** if last 5 sessions include a ≥5% up-day); if trend-up, upside leg from close ≥ 1.5× downside leg.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` ≥ `max(as-of, UTC-session high already printed)` + **0.5 × ATR-proxy**. Never park the high on a wick/magnet ($80k / $81.5k / $81500).
   - **Printed-low clearance:** `range_low` ≤ `min(as-of, UTC-session low already printed)` − **0.5 × ATR-proxy**.
   - **Weekend printed-extreme carry-forward (v1.16):** Sat/Sun and US holidays use the **last completed UTC session** high/low as the printed extreme, not today's thin weekend session. `range_high` ≥ last-completed-UTC high + applicable clearance; `range_low` ≤ last-completed-UTC low − applicable clearance. (Sep 12 BTC 1d cap $79,800 sat **under** Fri Yahoo H $79,818. Fade 0.75× off Fri H + last ETF outflow required ≥~$81,470.)
   - **Fade/outflow low+high clearance (v1.6/v1.7):** if `prior_day_pct` ≤ **−1.0** OR last completed US spot BTC/ETH ETF session is net outflow, use **0.75 × ATR-proxy** printed-low AND printed-high clearance. Applies even when the last ETF print is several sessions old (weekend/holiday).
   - **Post-fade stacked low (v1.14):** if the last **completed** UTC session is down **AND** last completed US spot ETF for that asset is net outflow, 1d printed-low clearance = **1.0 × ATR-proxy**. Stacks over 0.75× fade — use the larger clearance. (Sep 9 BTC 1d floor $77,500 vs req ≤~$76,410; path L $76,732 / C $77,158 missed.)
   - **ETF-flip extra high (v1.7):** last completed US spot BTC or ETH ETF session reversed sign vs prior session → +**0.5 × ATR-proxy** extra to that asset's 1d `range_high`.
   - **Post-impulse high clearance (v1.8):** prior completed UTC session ≥ **+5%** OR live impulse ≥ **+3%** / **1.0 × ATR** → 1d printed-high clearance = **1.0 × ATR-proxy**. (Sep 3 BTC 1d cap $81,000 vs path H $82,300.)
   - **Mega-inflow extra high (v1.8):** last completed US spot BTC ETF ≥ **+$400M** → +0.5×ATR to BTC 1d and 1w high. ETH ETF ≥ **+$100M** → same for ETH. Stacks with ETF-flip and weekend-carry. (Sep 11 ETH +$216.4M.)
   - **Spike-fade:** wick ≥ 0.8×ATR is not a cap; still apply 0.5×ATR clearance above that high.
   - **RANGE_CHECK (v1.16 — hard).** Immediately after the parseable table and before `TRACKER_SHA`, print one line:
     `RANGE_CHECK: BTC ATR $A; 1d width $W vs 2.0×=$M; high $H vs req $R; low $L vs req $K; fade/outflow 0.75x yes/no; stacked-low 1.0x yes/no; weekend-carry yes/no. ETH ATR $A2; width $W2 vs $M2; high $H2 vs req $R2; low $L2 vs req $K2; fade 0.75x yes/no; stacked-low 1.0x yes/no; weekend-carry yes/no.`
     If 1d width < 2.0×ATR **or** `range_high` < required printed-high **or** `range_low` > required printed-low, **widen and reprint the table** before writing.
4. Fill **pred_regime** and **prior_day_pct** on every tracker row. Put the **as-of UTC timestamp** in 1d notes.
   - **conf** is an integer **40–85**, never a 0.xx decimal. (Sep 11/12 Daily wrote 0.55/0.58.)
   - **prior_day_pct (v1.16):** last **completed UTC daily close-to-close %** only. Print `source: YYYY-MM-DD $c1 → YYYY-MM-DD $c2 = Z%`. Never reuse yesterday's Daily figure. Never use live-session %, 24h change, or live-to-prior-close. (Sep 10 reused Sep 8 −0.8/−0.2 vs true Sep 8→9 Yahoo −0.23/−1.17. Sep 11 wrote −1.62/−1.97 vs true Sep 9→10 BTC −2.16% / ETH −1.21%. Sep 12 wrote ETH +7.25 vs true Sep 10→11 Yahoo $2,437→$2,515 = **+3.19%**.)
5. Include **prior-scenario vs actual** from the tracker when closed rows exist.
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first:** immediately after Key Takeaway, 8-row table (asset, horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, prior_day_pct). Entire table + `RANGE_CHECK:` + `TRACKER_SHA:` line in first ~1400 characters.
8. **Weekend/holiday ETF:** Sat/Sun and US market holidays have no US spot ETF print. State last completed session date and figure. **Last completed as of 2026-09-12 = Fri 2026-09-11 BTC −$13.2M / ETH +$216.4M.** 10 Sep BTC −$282.7M / ETH −$29.9M. Labor Day 2026-09-07 = no print. Do not invent 0.0 as a completed session.
9. **Weekend writes are mandatory.** Saturday and Sunday must append 8 tracker rows for that `analysis_date`.
10. **Write-first:** commit the 8 tracker rows immediately after the parseable table — before long narrative.
11. **Write-SHA gate (hard).** After the table: get tracker SHA → merge 8 rows into existing body → re-get. Do not write snapshot until response contains the new **blob SHA**. `WRITE PENDING` is banned.
12. **Write is the first tool sequence.** First tool calls = `get_file_contents` on tracker then `push_files` FULL MERGED body. If SHA unchanged, `create_or_update_file` same body. **SHA-delta:** emitted SHA must differ from pre-write SHA. Runtime is irrelevant — Sep 1 through Sep 12 Daily wrote 0 durable rows (write-streak **14**).
13. **Price-quote cap.** After the two GitHub reads, at most one quote batch (Yahoo BTC-USD + ETH-USD + Farside last completed session). As-of = that live quote. Quote ≤20 minutes old. Title-quote match: BTC within $1,000 of as-of; ETH within $30. If a second print within 20 min differs BTC ≥$1,000 or ETH ≥$30, re-quote once before lock. NEXT call is the tracker write. (Sep 11 locked ETH $2,500 vs Coinbase $2,594.)
14. **Write-streak emergency ON (streak 14).** After the two reads + one quote batch, ONLY GitHub write tools until a new 40-char blob SHA exists. Sub-90s no new SHA = WRITE FAILED.
    - **push_files-first:** first write tool is `push_files` with the **full merged markdown**. Do not lead with `create_or_update_file`.
15. **Append-only / anti-wipe (hard).**
    - **Never** replace the tracker with only today's 8 rows. Merge into existing body. Preserve every prior row including `pred_regime` / `prior_day_pct` / closed actuals.
    - **Never** write `PLACEHOLDER` or `SEE_LOCAL_FULL_FILE`. Both are wipes. Sep 7 audit wiped to PLACEHOLDER. Sep 10/11 audits wrote SEE_LOCAL_FULL_FILE (header-only blob `497d68df`). Restore source = commit `87e37a2` / blob `08175782`.
    - After `get_file_contents`, if tracker body is `PLACEHOLDER` / `SEE_LOCAL_FULL_FILE` / fewer than 20 data rows, **do not overwrite**. Emit `WRITE FAILED` plus today's 8 rows. Restoration is Auditor-only.
    - After write, re-get row-count must be `prior_count + 8` (or `prior_count` if today's 8 already existed). A post-write body with only 8 data rows or header-only is WRITE FAILED.
    - Payload-compact: if write rejects size, shorten CLOSED notes only; keep every row; retry. Never emit SEE_LOCAL_FULL_FILE.
    - Do not change ranges or `pred_*` on already-open prior-day rows. Path-refresh of actuals on open rows is allowed.

## Report structure

**Key Takeaway** (one sentence)

**Parseable table** (8 rows)

`RANGE_CHECK: ...` (v1.16; must pass or reprint table)

`TRACKER_SHA: <blob sha>` (40-char hex that **differs** from the pre-write SHA)

1. Current Market Snapshot
2. Technical Analysis — levels, MAs, RSI, ATR-proxy, regime
3. Fundamental & News — ETF flows with session date; catalysts with probability + timing
4. Forward Scenarios — BTC/ETH 1d/1w/1m/3m $low–$high (bias; conf); invalidation; prior vs actual
5. Decision map (3 bullets)
6. Risks & Disclaimer — not financial advice

## GitHub write (mandatory — hard gate)

Get SHA immediately before write; retry once on conflict.

- Merge one row per (analysis_date, asset, horizon) for BTC and ETH × {1d, 1w, 1m, 3m}. Status = open.
- Do not duplicate (analysis_date, asset, horizon). Do not change ranges on already-open prior-day rows.
- Dual-write full merged body. SHA-delta. Anti-wipe row-count gate.
- Response must include `TRACKER_SHA: <sha>` (40-char hex, different from pre-write). Never write `WRITE PENDING`.

Cite sources. Be objective and data-driven.
