# SPCX Daily Analysis Prompt

**Version:** 1.37  
**Last edited:** 2026-10-09T15:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first. After the table: `get_file_contents` tracker → write today's 4 rows + path refresh with the **full table body**. Prefer `push_files`. Main is PR-protected — on 409 open branch `spcx-daily-YYYYMMDD` and a PR. TRACKER_SHA must differ from pre-write SHA. Email is not a write. Never push a header-only tracker, TRACKER_BODY pointer, PLACEHOLDER, SEE_FILE, or prompt stub. Outbound tracker ≥ inbound row count and ≥64 data rows and ≥15kB.
3. If today's 4 rows already exist: PREEXISTING_ROWS + current blob SHA. Do not duplicate existing dates. Do not rewrite locked 9/22–10/04 bands. Do not reopen Auditor 10/09 closes (10/02–10/04 1d, 9/28–10/01 1w, 9/03–9/09 1m). Do not invent missing 10/05–10/08 analysis rows.
4. Anti-wipe: outbound tracker ≥ inbound row count and ≥64 `| 2026-` rows and ≥15kB. Pre-write abort if the exact payload is below those floors. Never header-only. Streak 0. Daily inserts session-day rows; Auditor grades/path-refreshes/closes only. Post-write verify raw body. Each data row must have 18 pipe-separated fields.
5. Restore a stub prompt (<2kB / missing Process rules) to this v1.37 body before using it. Abort SHAs: `daf3296c` (109-line wipe), `b3815b67` (header-only blob), `547fe344` (PLACEHOLDER). v1.33–v1.36 never landed on main — this v1.37 file wins.

## Range / regime

- ATR-proxy: last-5 TR median vs 14d mean TR; if they differ <20%, use the last-5 median. After 10/08 official: last-5 H-L 7.60/5.66/5.03/13.85/10.50 → median **$7.60**; 14d mean H-L **$6.38**; differ ~19% <20% → use **$7.60**. Do not reuse the 10/02 $5.44 figure. Recompute after the next official EOD.
- 1d width ≥2.0× ATR; 1w ≥3.0× (≥4.0× if last 5 sessions include ≥+5% OR widen-high is ON). 10/05 was +7.63% and widen-high is ON, so next 1w width ≥4.0× ATR ($30.40).
- Never park 1d/1w high on $166 / $170 / $172 / $176 / $180 / $185 / $190. Closed 1d misses now include 10/02 H172.47>166, 10/03 H172.47>170, 10/04 H172.47>170. 1d hit rate after 10/09 audit: 24/30.
- Widen-high ON: last 3 closed 1w (9/29, 9/30, 10/01) all upper-exceed (path H$176.42 vs 174/175/176). Next 1d/1w high ≥ **$191.62** (176.42+2.0×$7.60). 1d/1w low ≤ **$152.40** (160.00−1.0×$7.60). Hard-fail reprint if short. Stay ON until 2 consecutive closed 1w are not upper-exceed.
- 10/09 unlock is in-session as of this audit. After 10/09 official, next dated unlock **2026-10-24** is outside the next 10 RTH — drop known-event extra unless a new dated event enters that window.
- pred_rel_vol vs 20d official volume only. prior_day_pct from last official close. After 10/08 official: Rel Vol ~71.9M / 20d ~90M **below-avg**; prior_day_pct **−4.19**.
- Regime from last official close location / impulse, not live mid-prints. 10/08 close −4.19% is not a fresh ≥+5% trend-up force. Bias midpoint must still sit above C$160.57 while the open 1w window contains the 10/05–10/06 spike. Do not relabel locked 10/02 digestion or 10/03–10/04 trend-up rows.
- 1d maps to the next RTH. Weekend analysis_date 1d also maps to the next RTH. 1d actuals are that next session only. Do not close 1w/1m mid-session. Do not close 10/02–10/04 1w or 9/10 1m until 10/09 regular close.
- Last 3 closed 1w as of 9 Oct audit (9/29, 9/30, 10/01) are all upper-exceed — widen-high / 2.0× ATR-on-path-high rule ON.

## Path + close-clock (v1.37)

- Path H/L/C for a row = official extremes from **that analysis_date session** through last official (or through horizon close). Weekend as-of = last official session. Do **not** inherit another row's path high. Closed clocks stay session-isolated (9/28 1w H$172.47, 9/29–10/01 1w H$176.42, 9/03 1m H$172.47, 9/04–9/09 1m H$176.42). Open rows whose window includes 10/06 use path high **$176.42**, last close **$160.57**.
- Header must print **1m Day N/21** for the oldest open 1m. Oldest open 1m after Auditor 10/09: **9/10 1m Day 20/21** (closes 10/09 — do not close mid-session).
- Auditor closed on 2026-10-09 (official through 10/08 only; 10/09 mid-session not final): 10/02 1d MISS upper (140-166, H172.47, dir no, err 9.7%); 10/03 1d MISS upper (142-170, dir yes, err 6.6%); 10/04 1d MISS upper (142-170, dir yes, err 5.6%); 9/28 1w HIT (132-173, H172.47 gap 0.53, dir yes, err 15.6%); 9/29 1w MISS upper (132-174, H176.42, dir no, err 17.8%); 9/30 1w MISS upper (132-175, H176.42, dir no, err 14.0%); 10/01 1w MISS upper (132-176, H176.42 by 0.42, dir yes, err 6.3%); 9/03 1m HIT (120-185, C171.09); 9/04 1m HIT (120-190, C171.92); 9/08 1m HIT (120-195, C167.60); 9/09 1m HIT (115-195, C160.57).

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward 1d/1w/1m/3m; 3-bullet decision map; disclaimer. Self-check including widen-high floors 191.62/152.40 + bias midpoint above C160.57 + 18-field rows + hard-fail reprint yes/no + anti-wipe ≥64 / ≥15kB + path isolation + 1m Day N/21 header line.
