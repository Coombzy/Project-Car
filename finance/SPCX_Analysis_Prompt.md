# SPCX Daily Analysis Prompt

**Version:** 1.34
**Last edited:** 2026-10-06T15:25:00Z
**Owner:** Coombzy / Project-Car
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first. After the table: `get_file_contents` tracker → write today's 4 rows + path refresh with the **full table body**. Prefer `push_files`. Main is PR-protected (409): push a branch and open a PR if direct main write is rejected; do not emit a TRACKER_SHA for a write that did not land. Email is not a write. Never push a header-only tracker, TRACKER_BODY pointer, PLACEHOLDER, SEE_FILE, or prompt stub. Outbound tracker ≥ inbound row count and ≥64 data rows and ≥15kB.
3. If today's 4 rows already exist: PREEXISTING_ROWS + current blob SHA. Do not duplicate 9/22 through 10/04 rows. Do not rewrite locked 9/14, 9/16, 9/18, 9/22–10/04 bands. Do not reopen Auditor 10/06 closes (9/03 1m, 9/28 1w, 10/02 1d, 10/03 1d, 10/04 1d) or Auditor 10/03 closes (9/02 1m, 9/25–9/27 1w, 10/01 1d).
4. Anti-wipe: outbound tracker ≥ inbound row count and ≥64 `| 2026-` rows and ≥15kB. Pre-write abort if the exact payload is below those floors. Never header-only. Streak 0. Daily inserts session-day rows; Auditor grades/path-refreshes/closes only. Post-write verify raw.githubusercontent.com main (or the PR head if main is protected); if stub / TRACKER_BODY / <15kB / <64 rows, restore-merge immediately and do not emit TRACKER_SHA. Each data row must have 18 pipe-separated fields. Hard-fail if status lands in pct_error.
5. Restore a stub prompt (<2kB / missing Process rules) to this v1.34 body before using it. Restore a header-only / <60-row tracker from commit `6127247be7f8ae96655d7098115b79bb292fa64a` / blob `5640951b51eacddee176c387a0fba7ebbf70c3d8` (fallback `3afe8900814f026f09f7dfd57c479a7a311626f9` / `d0afc402b6d082e8f1fe071ed83423c13f8b5d62`) before writing. Abort SHAs: `daf3296c` (109-line wipe), `b3815b67` (header-only blob), `547fe344` (PLACEHOLDER). Do not treat the 2026-10-06 full table as a stub. The 2026-10-05 mid-session automation note (live H168.50, floor 176.66, do-not-close) is superseded by this v1.34 official close.

## Range / regime

- ATR-proxy: last-5 TR median vs 14d mean TR; if they differ <20%, use the last-5 median. After 10/05 official: last-5 H-L 13.85/10.50/7.75/4.83/4.59 → median **$7.75**; 14d mean H-L **$6.47**; differ ~19.8% <20% → use **$7.75**. Do not reuse the 10/02 $5.44 figure or the 10/01 $4.83 figure. Recompute after the next official EOD.
- 1d width ≥2.0× ATR; 1w ≥3.0× (≥4.0× only if last 5 sessions include ≥+5%). 10/05 official close was +7.63% vs 10/02 C$158.96, so the next insert uses trend-up and 1w width ≥4.0× ATR. Do not rewrite locked 10/02, 10/03, or 10/04 bands. Next insert after a new ≥+5% close repeats the 4.0× rule; otherwise revert 1w to 3.0×.
- Impulse-continuation (v1.34, Auditor 10/06): if the last official close is ≥+5% AND that session's H-L is ≥1.5× the ATR-proxy used for the prior insert, the next 1d range_high must be ≥ that session high + **2.5×** the newly recomputed ATR-proxy. +1.0× and +2.0× both failed the 10/05 print: 10/02 H$159.84 +1.0×$5.44 = $165.28 (printed 170 on 10/03 and 10/04) vs official H$172.47. +2.5×$5.44 = $173.44 would have contained it. After 10/05 the floor is **$191.85** (172.47+2.5×$7.75). Hard-fail reprint if the new 1d high is below that floor or parked on $166 / $170 / $172 / $176 / $180.
- Never park 1d/1w high on $149 / $150 / $155 / $156 / $157 / $159 / $160 / $166 / $170 / $172. Closed 1d misses: 9/02 H152.30>149, 9/14 L142.87<143, 9/16 H156.87>156, 10/02 H172.47>166, 10/03 H172.47>170, 10/04 H172.47>170. 1d hit rate after 10/06 audit: 24/30.
- After each official EOD, recompute printed extremes then restack. Base stack remains +1.0× ATR on 1d/1w (high ≥ **$180.22**, low ≤ **$150.87**). The impulse-continuation rule above overrides the 1d high when it fires. 10/03 and 10/04 printed 142–170 — locked, do not reprint them tighter or wider.
- Keep known-event extra while the next dated unlock sits inside the next 10 RTH. Next dated unlock **2026-10-09** remains inside that window as of Tue 10/06.
- pred_rel_vol vs 20d official volume only. prior_day_pct from last official close. Do not bucket Rel Vol off mid-session volume. After 10/05 official: Rel Vol ~134.7M / 20d ~98M ≈ 1.37x **elevated**; prior_day_pct **+7.63**.
- Regime from last official close location / impulse, not live mid-prints. 10/05 close +7.63% ≥+5% → next insert is trend-up, not digestion. Do not relabel locked 10/02 digestion rows.
- After a ≥+5% official close, the next insert must set 1d and 1w bias midpoint above that close. Do not center bias below a +5% print. 10/02 1d was a directional miss (bias mid $156 below prior C$158.96, close $171.09). 10/03 and 10/04 bias mids were above $158.96 and directional HIT, but the range high still missed.
- 1d maps to the next RTH. Weekend analysis_date 1d also maps to the next RTH. 1d actuals are that next session only — do not store the analysis-session OHLC as the 1d window. Do not close 1w/1m mid-session; Auditor marks Day N/5 and Day N/21 closes. 10/06 is mid-session as of this edit — do not close 9/29 1w or 9/04 1m.
- Last 3 closed 1w as of 6 Oct audit (9/26, 9/27, 9/28) are all HIT, none upper-exceed (9/28 path H$172.47 vs 173, gap 0.53) — widen-high / extra 1w ATR rule OFF. The separate ≥+5% close rule and the v1.34 1d +2.5× impulse-continuation rule are ON for the next insert.

## Path + close-clock (v1.34)

- Path H/L/C for a row = official extremes from **that analysis_date session** through last official (or through horizon close). Weekend as-of = last official session. Do **not** inherit another row's path high. Closed clocks stay session-isolated (9/22 1w H$154.94, 9/23 1w H$154.26, 9/24 1w H$153.78, 9/25–9/27 1w H$159.84, 9/02 1m H$159.84). Open rows whose window includes 10/05 use path high **$172.47** and last **$171.09**.
- Header must print **1m Day N/21** for the oldest open 1m and any 1m/3m that hits its close clock on last official (21st / 63rd RTH after analysis_date). 1w Day N/5 counts RTH **after** analysis_date, not including it.
- Auditor closed on 2026-10-06 (10/05 official O158.99 H172.47 L158.62 C171.09): 9/03 1m (clock 10/05 C171.09 HIT, range 120-185, dir yes, err 10.4%), 9/28 1w (clock 10/05 C171.09 H172.47 HIT, range 132-173, not upper-exceed, dir yes, err 15.6%), 10/02 1d MISS upper-exceed (140-166, dir no, err 9.7%), 10/03 1d MISS upper-exceed (142-170, dir yes, err 6.6%), 10/04 1d MISS upper-exceed (142-170, dir yes, err 5.6%). Oldest open 1m after that close: **9/04 1m Day 20/21** (closes 10/06 — do not close mid-session). 9/29 1w Day 4/5 closes 10/06 — do not close early.

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward 1d/1w/1m/3m; 3-bullet decision map; disclaimer. Self-check including impulse-continuation floor 191.85 / base stack 180.22/150.87 + bias midpoint above a +5% close + 18-field rows + hard-fail reprint yes/no + anti-wipe ≥64 / ≥15kB + path isolation + 1m Day N/21 header line.
