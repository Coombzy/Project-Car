# SPCX Daily Analysis Prompt

**Version:** 1.32  
**Last edited:** 2026-10-03T15:25:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first. After the table: `get_file_contents` tracker → write today's 4 rows + path refresh with the **full table body**. Prefer `push_files` for the tracker (create_or_update_file truncated 109 lines at `daf3296c` on 2026-09-30). TRACKER_SHA must differ from pre-write SHA. Email is not a write. Never push a header-only tracker, TRACKER_BODY pointer, PLACEHOLDER, SEE_FILE, or prompt stub. Outbound tracker ≥ inbound row count and ≥64 data rows and ≥15kB.
3. If today's 4 rows already exist: PREEXISTING_ROWS + current blob SHA. Do not duplicate 9/22, 9/23, 9/24, 9/25, 9/26, 9/27, 9/28, 9/29, 9/30, 10/01, 10/02, or 10/03 rows. Do not rewrite locked 9/14, 9/16, 9/18, 9/22, 9/23, 9/24, 9/25, 9/26, 9/27, 9/28, 9/29, 9/30, 10/01, 10/02, 10/03 bands. Do not reopen Auditor 10/03 closes (9/02 1m, 9/25–9/27 1w, 10/01 1d).
4. Anti-wipe: outbound tracker ≥ inbound row count and ≥64 `| 2026-` rows and ≥15kB. Pre-write abort if the exact payload is below those floors. Never header-only. Streak 0. Daily inserts session-day rows; Auditor grades/path-refreshes/closes only. Post-write verify raw.githubusercontent.com main; if stub / TRACKER_BODY / <15kB / <64 rows, restore-merge immediately and do not emit TRACKER_SHA. Each data row must have 18 pipe-separated fields. Hard-fail if status lands in pct_error (Auditor repaired the short 10/03 1d pipe).
5. Restore a stub prompt (<2kB / missing Process rules) to this v1.32 body before using it. Restore a header-only / <60-row tracker from commit `6127247be7f8ae96655d7098115b79bb292fa64a` / blob `5640951b51eacddee176c387a0fba7ebbf70c3d8` (fallback `3afe8900814f026f09f7dfd57c479a7a311626f9` / `d0afc402b6d082e8f1fe071ed83423c13f8b5d62`) before writing. Abort SHAs: `daf3296c` (109-line wipe), `b3815b67` (header-only blob), `547fe344` (PLACEHOLDER). Do not treat the 2026-10-03 full table (blob `54cdbd58dbb3ee4420da9bc2bd09885f0f04e690`, ~116 rows) as a stub.

## Range / regime

- ATR-proxy: last-5 TR median vs 14d mean TR; if they differ <20%, use the last-5 median. After 10/02 official: last-5 H-L 10.50/7.75/4.83/4.59/5.44 → median **$5.44**; 14d mean H-L **$5.89**; differ ~8% <20% → use **$5.44**. Do not reuse the 10/01 $4.83 figure or the 9/30 $4.59 figure. Recompute after the next official EOD.
- 1d width ≥2.0× ATR; 1w ≥3.0× (≥4.0× only if last 5 sessions include ≥+5%). 10/02 official close was +7.35% vs 10/01 C$148.07, so the 10/03 insert used trend-up and 1w width ≥4.0× ATR. Do not rewrite locked 10/02 or 10/03 bands. Next insert after a new ≥+5% close repeats the 4.0× rule; otherwise revert 1w to 3.0×.
- Never park 1d/1w high on $149 / $150 / $155 / $156 / $157 / $159 / $160. Closed 1d misses remain 9/02 H152.30>149, 9/14 L142.87<143, 9/16 H156.87>156 — all tight-range breaches. 1d hit rate after 10/03 audit: 24/27 (10/01 1d HIT, H159.84 inside 161, gap 1.16).
- After each official EOD, recompute printed extremes then restack +1.0× ATR on 1d/1w. After 10/02 official stacked floors: 1d/1w high ≥ **$165.28** (159.84+1.0×$5.44); 1d/1w low ≤ **$143.90** (149.34−1.0×$5.44). Hard-fail reprint if short. 10/03 printed 1d 142–170 / 1w 130–192 already clears these floors — do not reprint them tighter.
- Keep known-event extra while the next dated unlock sits inside the next 10 RTH. Next dated unlock **2026-10-09** remains inside that window as of Sat 10/03.
- pred_rel_vol vs 20d official volume only. prior_day_pct from last official close. Do not bucket Rel Vol off mid-session volume. After 10/02 official: Rel Vol ~119.54M / 20d ~94.2M ≈ 1.27x **elevated**; prior_day_pct **+7.35**.
- Regime from last official close location / impulse, not live mid-prints. 10/02 close +7.35% ≥+5% → 10/03 insert is trend-up, not digestion. Do not relabel locked 10/02 digestion rows.
- After a ≥+5% official close, the next insert must set 1d and 1w bias midpoint above that close. Do not center bias below a +5% print. 9/25–9/27 1w were range HIT but directional miss: bias mid $148 sat below prior close $148.68 while the path finished at $158.96. 10/03 bias 155–166 / 152–178 already clears C$158.96 — do not rewrite.
- 1d maps to the next RTH. Weekend analysis_date 1d also maps to the next RTH. 1d actuals are that next session only — do not store the analysis-session OHLC as the 1d window. Do not close 1w/1m mid-session; Auditor marks Day N/5 and Day N/21 closes.
- Last 3 closed 1w as of 3 Oct audit (9/25, 9/26, 9/27) are all HIT, none upper-exceed (path H$159.84 vs 172/173) — widen-high / extra 4.0× ATR rule OFF. The separate ≥+5% close rule already applied to the 10/03 insert.

## Path + close-clock (v1.32)

- Path H/L/C for a row = official extremes from **that analysis_date session** through last official (or through horizon close). Weekend as-of = last official session. Do **not** inherit another row's path high. Closed clocks stay session-isolated (9/22 1w H$154.94, 9/23 1w H$154.26, 9/24 1w H$153.78, pre-10/02 1m clocks keep H$158.13). Open rows whose window includes 10/02 use path high **$159.84**.
- Header must print **1m Day N/21** for the oldest open 1m and any 1m/3m that hits its close clock on last official (21st / 63rd RTH after analysis_date). 1w Day N/5 counts RTH **after** analysis_date, not including it.
- Auditor closed on 2026-10-03: 9/02 1m (clock 10/02 C158.96 HIT, range 110-180, dir yes, err 9.6%), 9/25 1w (clock 10/02 C158.96 H159.84 HIT, range 132-172, dir no, err 7.4%), 9/26 1w HIT dir no (132-173), 9/27 1w HIT dir no (132-173), 10/01 1d (maps to 10/02 RTH L149.34 H159.84 C158.96 HIT inside 139-161, dir yes, err 5.3%). Oldest open 1m after that close: **9/03 1m Day 20/21** (closes 10/05). 9/28 1w Day 4/5 closes after 10/05 — do not close early. 10/02 1d maps to 10/05 — do not close and do not store 10/02 OHLC as that 1d actual. 10/03 1d maps to 10/05.

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward 1d/1w/1m/3m; 3-bullet decision map; disclaimer. Self-check including stacked floors 165.28/143.90 + bias midpoint above a +5% close + 18-field rows + hard-fail reprint yes/no + anti-wipe ≥64 / ≥15kB + path isolation + 1m Day N/21 header line.
