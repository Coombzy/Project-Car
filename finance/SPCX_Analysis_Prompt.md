# SPCX Daily Analysis Prompt

**Version:** 1.29  
**Last edited:** 2026-10-01T16:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first. After the table: `get_file_contents` tracker → write today's 4 rows + path refresh with the **full table body**. Prefer `push_files` for the tracker (create_or_update_file truncated 109 lines at `daf3296c` on 2026-09-30). TRACKER_SHA must differ from pre-write SHA. Email is not a write. Never push a header-only tracker, TRACKER_BODY pointer, PLACEHOLDER, SEE_FILE, or prompt stub. Outbound tracker ≥ inbound row count and ≥64 data rows and ≥15kB.
3. If today's 4 rows already exist: PREEXISTING_ROWS + current blob SHA. Do not duplicate 9/22, 9/23, 9/24, 9/25, 9/26, 9/27, 9/28, 9/29, 9/30, or 10/01 rows. Do not rewrite locked 9/14, 9/16, 9/18, 9/22, 9/23, 9/24, 9/25, 9/26, 9/27, 9/28, 9/29, 9/30, 10/01.
4. Anti-wipe: outbound tracker ≥ inbound row count and ≥64 `| 2026-` rows and ≥15kB. Pre-write abort if the exact payload is below those floors. Never header-only. Streak 0. Daily inserts session-day rows; Auditor grades/path-refreshes/closes only. Post-write verify raw.githubusercontent.com main; if stub / TRACKER_BODY / <15kB / <64 rows, restore-merge immediately and do not emit TRACKER_SHA.
5. Restore a stub prompt (<2kB / missing Process rules) to this v1.29 body before using it. Restore a header-only / <60-row tracker from commit `6127247be7f8ae96655d7098115b79bb292fa64a` / blob `5640951b51eacddee176c387a0fba7ebbf70c3d8` (fallback `3afe8900814f026f09f7dfd57c479a7a311626f9` / `d0afc402b6d082e8f1fe071ed83423c13f8b5d62`) before writing. Abort SHAs: `daf3296c` (109-line wipe), `b3815b67` (header-only blob), `547fe344` (PLACEHOLDER).

## Range / regime

- ATR-proxy: last-5 TR median vs 14d mean TR; if they differ <20%, use the last-5 median. After 9/30 official: last-5 H-L 4.83/4.59/5.44/3.67/3.12 → median **$4.59**; 14d mean H-L **$5.48**; differ ~16% <20% → use **$4.59**. Recompute after the next official EOD. Do not reuse the 9/29 $6.02 branch.
- 1d width ≥2.0× ATR; 1w ≥3.0× (≥4.0× only if last 5 sessions include ≥+5%).
- Never park 1d/1w high on $149 / $150 / $155 / $156. Closed 1d misses remain 9/02 H152.30>149, 9/14 L142.87<143, 9/16 H156.87>156 — all tight-range breaches.
- After each official EOD, recompute printed extremes then restack +1.0× ATR on 1d/1w. After 9/30 official stacked floors: 1d/1w high ≥ **$157.17** (152.58+1.0×$4.59); 1d/1w low ≤ **$143.16** (147.75−1.0×$4.59). Hard-fail reprint if short.
- Keep known-event extra while the next dated unlock sits inside the next 10 RTH. Next dated unlock **2026-10-09** remains inside that window as of Thu 10/01.
- pred_rel_vol vs 20d official volume only. prior_day_pct from last official close. Do not bucket Rel Vol off mid-session volume. After 9/30 official: prior_day_pct **+1.09**, Rel Vol ~79.03M / 20d ~93.3M ≈ 0.85x **normal**.
- Regime from last official close location / impulse, not live mid-prints. 9/30 close $150.86 inside the recent coil → digestion unless a completed session is ≥+5% or live impulse ≥+3% after the next official.
- 1d maps to the next RTH. Weekend analysis_date 1d also maps to the next RTH. Do not close 1w mid-session; Auditor marks Day N/5 closes. 10/01 is mid-session until 10/01 RTH close — do not close 9/30 1d or 9/24 1w on a mid-session print.
- Last 3 closed 1w as of 1 Oct audit (9/18, 9/22, 9/23) are all HIT, none upper-exceed — widen-high / 4.0× ATR rule OFF.

## Path + close-clock (v1.29)

- Path H/L/C for a row = official extremes from **that analysis_date session** through last official (or through horizon close). Weekend as-of = last official session. Do **not** inherit another row's path high (e.g. do not copy 9/21 H$158.13 onto 9/22+ 1m/3m). 9/24+ path high is session-isolated **$152.58** (9/30), not 9/21 and not 9/28 H$150.80.
- Header must print **1m Day N/21** for the oldest open 1m and any 1m/3m that hits its close clock on last official (21st / 63rd RTH after analysis_date). 1w Day N/5 counts RTH **after** analysis_date, not including it.
- Auditor closed on 10/01 audit (horizon-end close, not latest print): 8/26 1m after 9/25; 8/27 1m after 9/28 C145.47; 8/28 1m and 8/29 1m after 9/29 C149.24; 8/31 1m after 9/30 C150.86; 9/22 1w after 9/29 C149.24; 9/23 1w after 9/30 C150.86; 1d 9/25–9/29. Oldest open 1m: **9/02**. 9/24 1w Day 4/5 closes after 10/01 RTH — Daily does not close it mid-session. 9/30 1d maps to 10/01 and stays open until that RTH close.

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward 1d/1w/1m/3m; 3-bullet decision map; disclaimer. Self-check including stacked floors + hard-fail reprint yes/no + anti-wipe ≥64 / ≥15kB + path isolation + 1m Day N/21 header line.
