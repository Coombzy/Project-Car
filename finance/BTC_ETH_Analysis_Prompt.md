# BTC / ETH Daily Analysis Prompt

**Version:** 1.21  
**Last edited:** 2026-09-16T15:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** BTC ETH Daily Crypto Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **BTC and ETH** with **numeric range bands** (not point targets only) that can be graded later:

- Hit = path high/low **and** as-of close stayed inside the **range** over the horizon window (crypto is 24/7; **1d = 24h from as-of**, not NYSE close).
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.

## Process rules (always apply)

1. **ATR-proxy (v1.17)** — median true range of last 5 **completed weekday** UTC sessions. Exclude Sat/Sun and US-holiday thin sessions. Or published 14d ATR. State dollar value for BTC and ETH. (Weekday-5 incl. 9/10/11/12/15 Sep: BTC median ~$2,100; ETH ~$85. Recalc each run.)
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
   - **Weekend printed-extreme carry-forward (v1.16):** Sat/Sun and US holidays use the **last completed UTC session** high/low as the printed extreme, not today's thin weekend session. `range_high` ≥ last-completed-UTC high + applicable clearance; `range_low` ≤ last-completed-UTC low − applicable clearance. (Sep 12 BTC 1d cap $79,800 sat **under** Fri Yahoo H $79,818. Fade 0.75× off Fri H + last ETF outflow required ≥~$81,470.)
   - **Fade/outflow low+high clearance (v1.6/v1.7):** if `prior_day_pct` ≤ **−1.0** OR last completed US spot ETF **for that asset** is net outflow, use **0.75 × ATR-proxy** printed-low AND printed-high clearance. Applies even when the last ETF print is several sessions old (weekend/holiday).
   - **Post-fade stacked low (v1.14):** if the last **completed** UTC session is down **AND** last completed US spot ETF for that asset is net outflow, 1d printed-low clearance = **1.0 × ATR-proxy**. Stacks over 0.75× fade — use the larger clearance. (Sep 9 BTC 1d floor $77,500 vs req ≤~$76,410; path L $76,732 / C $77,158 missed.)
   - **ETF-flip extra high (v1.7):** last completed US spot BTC or ETH ETF session reversed sign vs prior session → +**0.5 × ATR-proxy** extra to that asset's 1d `range_high`.
   - **Post-impulse high clearance (v1.8):** prior completed UTC session ≥ **+5%** OR live impulse ≥ **+3%** / **1.0 × ATR** → 1d printed-high clearance = **1.0 × ATR-proxy**. (Sep 3 BTC 1d cap $81,000 vs path H $82,300.)
   - **Live-impulse low clearance (v1.20):** if at as-of, (UTC-session open − spot) ≥ **3%** OR ≥ **1.0 × ATR-proxy**, 1d printed-low clearance = **1.0 × ATR-proxy**. Symmetric to v1.8 post-impulse high. Stacks: use the larger of this 1.0× and stacked-low/fade 0.75×. (15 Sep live: BTC open $78,181 → ~$75,998 = −2.8%/1.06×ATR; ETH open $2,515 → $2,412 = −4.1%/1.32×ATR. Last UTC was up + ETF inflow so v1.14 stacked-low did not fire. Sep 15 Daily 1d floor $74,800 vs req ≤~$73,600 — construction miss; path L $74,945 still HIT.)
   - **Mega-inflow extra high (v1.8):** last completed US spot BTC ETF ≥ **+$400M** → +0.5×ATR to BTC 1d and 1w high. ETH ETF ≥ **+$100M** → same for ETH. Stacks with ETF-flip and weekend-carry. (14 Sep ETH +$121.1M; 11 Sep ETH +$216.4M.)
   - **Known-macro extra high (v1.19):** CPI/PCE/FOMC/NFP extra applies only if the **event timestamp** is ≤ as-of+24h, not if the calendar day is tomorrow. FOMC 16 Sep 18:00Z is **not** inside 24h of a 15 Sep ~14:36Z as-of (~27h). Do not add +0.5×ATR for FOMC on a 15 Sep run. Sep 16 Daily ~14:07Z as-of **is** inside 24h of FOMC 18:00Z — apply the extra then.
   - **Spike-fade:** wick ≥ 0.8×ATR is not a cap; still apply 0.5×ATR clearance above that high.
   - **RANGE_CHECK (v1.17/v1.20 — hard).** Immediately after the parseable table and before `TRACKER_SHA`, print one line:
     `RANGE_CHECK: BTC ATR $A (weekday-5); 1d width $W vs 2.0×=$M; high $H vs req $R; low $L vs req $K; fade/outflow 0.75x yes/no; stacked-low 1.0x yes/no; live-impulse-low 1.0x yes/no; weekend-carry yes/no. ETH ATR $A2 (weekday-5); width $W2 vs $M2; high $H2 vs req $R2; low $L2 vs req $K2; fade 0.75x yes/no; stacked-low 1.0x yes/no; live-impulse-low 1.0x yes/no; weekend-carry yes/no.`
     If 1d width < 2.0×ATR **or** `range_high` < required printed-high **or** `range_low` > required printed-low, **widen and reprint the table** before writing.
4. Fill **pred_regime** and **prior_day_pct** on every tracker row. Put the **as-of UTC timestamp** in 1d notes.
   - **conf** is an integer **40–85**, never a 0.xx decimal and never below 40. (Sep 11/12 Daily wrote 0.55/0.58. Sep 12 3m wrote 35.)
   - **prior_day_pct (v1.17):** last **completed UTC daily close-to-close %** from **Yahoo BTC-USD / ETH-USD official daily Close** only. Print `source: Yahoo YYYY-MM-DD $c1 → YYYY-MM-DD $c2 = Z%`.
   - **Banned sources:** tracker `actual_close`, path-refresh Last, live-session %, 24h change, live-to-prior-close, or yesterday's Daily figure.
   - (Sep 14 was clean: Yahoo Sep 12→13 BTC $77,270.47→$76,838.16 = **−0.56%** / ETH $2,525.94→$2,477.02 = **−1.94%**. Sep 15 Yahoo Sep 13→14 BTC $76,838.16→$78,163.38 = **+1.72%** / ETH $2,477.02→$2,515.17 = **+1.54%**. Sep 16 Yahoo Sep 14→15 BTC $78,163.38→$75,612.51 = **−3.26%**.)
5. Include **prior-scenario vs actual** from the tracker when closed rows exist.
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first:** immediately after Key Takeaway, 8-row table (asset, horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, prior_day_pct). Entire table + `RANGE_CHECK:` + `TRACKER_SHA:` line in first ~1400 characters.
8. **Weekend/holiday ETF:** Sat/Sun and US market holidays have no US spot ETF print. State last completed session date and figure. **Last completed as of 2026-09-16 = Tue 2026-09-15 BTC −$450.4M / ETH −$142.3M.** 14 Sep BTC +$159.9M / ETH +$121.1M. 11 Sep BTC −$13.2M / ETH +$216.4M. 10 Sep BTC −$282.7M / ETH −$29.9M. Labor Day 2026-09-07 = no print. Wed 16 Sep Farside dashes / 0.0 is a placeholder — not a completed session. Do not invent 0.0 as a completed session.
9. **Weekend writes are mandatory.** Saturday and Sunday must append 8 tracker rows for that `analysis_date` **only if those 8 rows do not already exist**.
10. **Write-first:** commit the 8 tracker rows immediately after the parseable table — before long narrative.
11. **Write-SHA gate (hard).** After the table: get tracker SHA → merge 8 rows into existing body → re-get. Do not write snapshot until response contains the new **blob SHA**. `WRITE PENDING` is banned.
12. **Write is the first tool sequence.** First tool calls = `get_file_contents` on tracker then `push_files` FULL MERGED body. If SHA unchanged, `create_or_update_file` same body. **SHA-delta:** emitted SHA must differ from pre-write SHA. Runtime is irrelevant — Sep 1 through Sep 16 Daily wrote 0 durable SHA-deltas that preserved history (write-streak **18**). Sep 13 Daily 14:26Z reused blob `9c84dd0f` after a partial-push wipe+restore. Sep 14 Daily commit `65182fba` deleted 127 lines from 126-row blob `79b6000a` and left header-only `d2c1cac8` (email: "Partial push wiped the table."). Sep 15 Daily title "BTC/ETH trend-down into FOMC" left SHA `bc737881` unchanged. Sep 16 Daily commits `e40e8d0` / `e0c7d92` / `9c29ced` claimed restore + 8 rows but left blob `c4a015cd` (1215B, 1 data row).
13. **Price-quote cap.** After the two GitHub reads, at most one quote batch (Yahoo BTC-USD + ETH-USD history Close + live Last + Farside last completed session). As-of = that live quote. Quote ≤20 minutes old. Title-quote match: BTC within $1,000 of as-of; ETH within $30. If a second print within 20 min differs BTC ≥$1,000 or ETH ≥$30, re-quote once before lock. NEXT call is the tracker write. (Sep 11 locked ETH $2,500 vs Coinbase $2,594.)
14. **Write-streak emergency ON (streak 18).** After the two reads + one quote batch, ONLY GitHub write tools until a new 40-char blob SHA exists. Sub-90s no new SHA = WRITE FAILED.
    - **push_files-first:** first write tool is `push_files` with the **full merged markdown**. Do not lead with `create_or_update_file`.
    - **Truncation fallback (v1.19 — hard).** `get_file_contents` truncates near ~20kB and cuts the ETH tail. If the body ends mid-row, omits today's expected ETH rows, or is shorter than the `size` field, immediately fetch `https://raw.githubusercontent.com/Coombzy/Project-Car/main/finance/BTC_ETH_Prediction_Tracker.md` (or a second get of the same path) and use **that** as inbound. **Never abort the write waiting for the ETH tail.** Sep 15 Daily read SHA `bc737881` (full file) then stalled on the truncated view and wrote 0 rows.
    - **Inbound-floor (v1.21 — hard).** Inbound data-row count MUST be ≥ **100** and inbound size ≥ **15kB** before any write. If main is header-only / PLACEHOLDER / SEE_LOCAL_FULL_FILE / 1-row / <100 data rows / <15kB, do **not** push that body. Fetch restore raw from commit `41e4ad58` / blob `47d11800e1f06a4fe5f5a5bc9279a0d5af8aa191` (2026-09-15 audit), merge today's 8 rows + allowed path-refresh, then push. Never emit a body with <100 data rows. Sep 16 Daily left 1-row blob `c4a015cd`.
    - **Preexisting-rows skip (v1.17):** if get_file_contents already contains today's 8 `(analysis_date, asset, horizon)` rows, do **not** rewrite the same body. Emit `PREEXISTING_ROWS` plus the current blob SHA. Do not claim SHA-delta.
    - **Outbound-row-count gate (v1.18 — hard).** Count inbound data rows from the **full** (non-truncated) body. The body you push MUST contain ≥ that count. If outbound < inbound, **do not call any write tool**. Emit `WRITE FAILED` plus today's 8 rows. Sep 14 Daily started from a full 126-row file and still wiped it — header-only / <20-row inbound abort is not enough.
15. **Append-only / anti-wipe (hard).**
    - **Never** replace the tracker with only today's 8 rows. Merge into existing body. Preserve every prior row including `pred_regime` / `prior_day_pct` / closed actuals.
    - **Never** write `PLACEHOLDER` or `SEE_LOCAL_FULL_FILE`. Both are wipes. Sep 7 audit wiped to PLACEHOLDER. Sep 10/11 audits wrote SEE_LOCAL_FULL_FILE (header-only blob `497d68df`). Restore source = commit `41e4ad58` / blob `47d11800e1f06a4fe5f5a5bc9279a0d5af8aa191` (2026-09-15 audit). Fallback commit `4d740d9` / blob `bc737881`. Older fallback commit `358a097` / blob `79b6000a`. Older fallback commit `87e37a2`.
    - After `get_file_contents`, if tracker body is `PLACEHOLDER` / `SEE_LOCAL_FULL_FILE` / fewer than 20 data rows, **do not overwrite**. Fetch the v1.21 restore blob, merge, then write. Emit `WRITE FAILED` plus today's 8 rows only if the restore fetch also fails. Restoration of a wiped main file **is** allowed for Daily when inbound <100 rows — that is a restore-merge, not an Auditor-only rewrite.
    - After write, re-get row-count must be `prior_count + 8` (or `prior_count` if today's 8 already existed; or restore_count + 8 if inbound was a wipe). A post-write body with only 8 data rows or header-only is WRITE FAILED.
    - Payload-compact: if write rejects size, shorten CLOSED notes only; keep every row; retry. Never emit SEE_LOCAL_FULL_FILE.
    - Do not change ranges or `pred_*` on already-open prior-day rows. Path-refresh of actuals on open rows is allowed.
    - **Role split (v1.17):** Daily **inserts** new `analysis_date` rows only. Auditor **grades / path-refreshes / closes** only. Auditor must **not** pre-insert the next Daily `analysis_date` 8-row block. Auditor **may** recover a Daily block that Daily already attempted and wiped.
16. **1d actuals = window-only (v1.17 — hard).** `actual_high` / `actual_low` / `actual_close` on a 1d row are the path inside the **24h window starting at that row's as-of**, not the last completed UTC session and not the multi-week path.
    - Never copy Fri H/L onto a Sat/Sun 1d row. (Sep 12 BTC 1d was path-refreshed with Fri Yahoo H $79,818 — that high is **pre-window**. Forward path H $77,480 / L $76,504 was a HIT inside $75,400–$79,800. Construction still failed weekend-carry.)
    - Construction uses last-completed-UTC printed extremes (v1.16). Grading uses the forward window. Do not mix them in the actual_* columns.
    - Sep 14 1d window 13:31Z Sep 14 → 13:31Z Sep 15: BTC H $79,569 / L $76,735 / C $76,525 HIT inside $74,200–$82,000. Post-window 15:04Z L BTC $75,684 / ETH $2,399 must **not** land on Sep 14 1d actuals.
    - Sep 15 1d window 14:36Z Sep 15 → 14:36Z Sep 16: BTC range $74,800–$82,100; Yahoo path L $74,945 / H $78,243 / C ~$75,690 = **HIT**. Construction still missed v1.20 live-impulse-low (req floor ≤~$73,600).

## Report structure

**Key Takeaway** (one sentence)

**Parseable table** (8 rows)

`RANGE_CHECK: ...` (v1.17/v1.20; must pass or reprint table)

`TRACKER_SHA: <blob sha>` (40-char hex that **differs** from the pre-write SHA, or `PREEXISTING_ROWS` + current SHA)

1. Current Market Snapshot
2. Technical Analysis — levels, MAs, RSI, ATR-proxy (weekday-5), regime
3. Fundamental & News — ETF flows with session date; catalysts with probability + timing
4. Forward Scenarios — BTC/ETH 1d/1w/1m/3m $low–$high (bias; conf); invalidation; prior vs actual
5. Decision map (3 bullets)
6. Risks & Disclaimer — not financial advice

## GitHub write (mandatory — hard gate)

Get SHA immediately before write; retry once on conflict.

- Merge one row per (analysis_date, asset, horizon) for BTC and ETH × {1d, 1w, 1m, 3m}. Status = open.
- Do not duplicate (analysis_date, asset, horizon). Do not change ranges on already-open prior-day rows.
- Dual-write full merged body. SHA-delta. Anti-wipe row-count gate. **v1.18 outbound-row-count ≥ inbound.** **v1.19 raw.githubusercontent fallback on truncation.** **v1.20 live-impulse low 1.0×ATR on live down ≥3% / ≥1.0×ATR.** **v1.21 inbound-floor ≥100 rows / ≥15kB; restore from 41e4ad58 / 47d11800 if wiped.**
- Response must include `TRACKER_SHA: <sha>` (40-char hex, different from pre-write) **or** `PREEXISTING_ROWS` if today's 8 already exist. Never write `WRITE PENDING`.

Cite sources. Be objective and data-driven.
