# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date` (Analysis runs mid-session). **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks (v1.3):** 1d = mapped next RTH close; **1w = 5th regular session after analysis_date**; 1m = 21st; 3m = 63rd. Weekend analysis_date starts the clock at the next RTH.

**Day N/5 (v1.8):** N = RTH sessions that have *begun after* `analysis_date` only. Do not count `analysis_date` itself (that is Day 0/5). After 2026-09-11 session begin: 9/03 1w Day 5/5 (still open until 9/11 official close), 9/04=4/5, 9/08=3/5, 9/09=2/5, 9/10=1/5, 9/11=0/5.

Status: `open` · `preliminary` · `closed` · `expired`  
Hit: actual H/L/Close (or path high/low over the horizon) stayed inside **range** (not only bias). Range bounds are inclusive.

Last price context: **2026-09-10 official RTH** (MarketWatch / YCharts / Yahoo) O **$145.00** H **$154.70** L **$144.89** C **$148.18** (+0.43%) Vol **~118.60M** (~1.45× vs last-20 RTH avg ~$82.0M = elevated). Last-5 median TR **$9.81**; 14d ATR ~$7.6 (use larger = $9.81). **2026-09-11 mid-session Yahoo ~12:11 ET** Last **$148.39** (+0.14%) O **$150.07** H **$150.59** L **$145.92** Vol **~38.7M** (incomplete). Path high **$155.00**. Closed 1d **9/10**; Closed 1w **6/6**. **Write-streak: 3** — 9/09 `write pending`; 9/10 `WRITE FAILED` (payload/schema); 9/11 SHA-reuse (emitted pre-write `6e4d34f3`). Emergency ON. Historical: 9/01 unrecoverable (no table); 9/02–04 recovered from email; 9/08 session-day write landed; 9/09–11 recovered from email.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next-session 8/27 RTH; H/L/C inside range |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 145.23 | 140.71 | yes | yes | 3.6% | closed | Day 5/5 after 2026-09-02 official; path L135.10 H145.23 C140.71 inside 120-155 |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L135.10 H155.00 Last148.39 inside |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L135.10 H155.00 Last148.39 inside |
| 2026-08-27 | 1d | 131 | 151 | 140 | 151 | 45 | digestion | below-avg | 0.89 | 137.90 | 143.29 | 141.50 | yes | yes | 2.7% | closed | next-session 8/28 official; L137.90 H143.29 C141.50 inside 131-151 |
| 2026-08-27 | 1w | 124 | 158 | 138 | 158 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 149.74 | yes | yes | 1.2% | closed | Day 5/5 after 2026-09-03 official; path L137.90 H152.30 C149.74 inside 124-158 |
| 2026-08-27 | 1m | 108 | 180 | 125 | 180 | 35 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L137.90 H155.00 Last148.39 inside |
| 2026-08-27 | 3m | 90 | 215 | 115 | 215 | 30 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L137.90 H155.00 Last148.39 inside |
| 2026-08-28 | 1d | 134 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.89 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | next-session 8/31 official; L139.88 H144.13 C143.69 inside 134-152 |
| 2026-08-28 | 1w | 124 | 162 | 140 | 162 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 147.95 | yes | yes | 2.0% | closed | Day 5/5 after 2026-09-04 official; path L137.90 H152.30 C147.95 inside 124-162 |
| 2026-08-28 | 1m | 105 | 188 | 125 | 188 | 35 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L137.90 H155.00 Last148.39 inside |
| 2026-08-28 | 3m | 85 | 225 | 115 | 225 | 30 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L137.90 H155.00 Last148.39 inside |
| 2026-08-29 | 1d | 132 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.45 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | weekend (pre-rule-10); next-session 2026-08-31 official; overlaps 8/28 1d |
| 2026-08-29 | 1w | 124 | 160 | 140 | 160 | 40 | digestion | below-avg | 0.45 | 137.90 | 152.30 | 147.95 | yes | yes | 1.3% | closed | Day 5/5 after 2026-09-04 RTH; path L137.90 H152.30 C147.95 inside 124-160 |
| 2026-08-29 | 1m | 105 | 190 | 125 | 190 | 35 | digestion | below-avg | 0.45 | 137.90 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L137.90 H155.00 Last148.39 inside |
| 2026-08-29 | 3m | 85 | 230 | 115 | 230 | 30 | digestion | below-avg | 0.45 | 137.90 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L137.90 H155.00 Last148.39 inside |
| 2026-08-31 | 1d | 131 | 148 | 138 | 148 | 35 | digestion | below-avg | 0.45 | 141.17 | 145.23 | 142.23 | yes | yes | 0.5% | closed | next-session 2026-09-01 official; L141.17 H145.23 C142.23 inside 131-148 |
| 2026-08-31 | 1w | 122 | 158 | 138 | 158 | 35 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 153.47 | yes | yes | 3.7% | closed | Day 5/5 after 2026-09-08 official; path L138.17 H155.00 C153.47 inside 122-158 |
| 2026-08-31 | 1m | 105 | 188 | 125 | 188 | 30 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L138.17 H155.00 Last148.39 inside |
| 2026-08-31 | 3m | 85 | 225 | 115 | 225 | 25 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L138.17 H155.00 Last148.39 inside |
| 2026-09-02 | 1d | 133 | 149 | 137 | 145 | 40 | digestion | below-avg | -1.02 | 141.05 | 152.30 | 149.74 | no | yes | 6.2% | closed | next-session 2026-09-03 official H152.30 > range_high 149 upper-exceed; first closed 1d miss; coil-spring post-dated |
| 2026-09-02 | 1w | 125 | 155 | 135 | 150 | 35 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 148.18 | yes | yes | 4.0% | closed | Day 5/5 after 2026-09-10 official; path L138.17 H155.00 C148.18 inside 125-155 inclusive cap |
| 2026-09-02 | 1m | 110 | 180 | 125 | 165 | 30 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L138.17 H155.00 Last148.39 inside |
| 2026-09-02 | 3m | 90 | 220 | 115 | 190 | 25 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L138.17 H155.00 Last148.39 inside |
| 2026-09-03 | 1d | 140 | 156 | 148 | 156 | 55 | digestion | below-avg | -1.07 | 147.32 | 150.85 | 147.95 | yes | no | 2.7% | closed | next-session 2026-09-04 official L147.32 H150.85 C147.95 inside 140-156; C below bias 148-156 |
| 2026-09-03 | 1w | 135 | 165 | 145 | 160 | 40 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 148.39 |  |  |  | open | Day 5/5; closes after 2026-09-11 official RTH; path thru 9/11 intra L141.05 H155.00 Last148.39 inside 135-165 |
| 2026-09-03 | 1m | 120 | 185 | 140 | 170 | 30 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L141.05 H155.00 Last148.39 inside |
| 2026-09-03 | 3m | 100 | 230 | 130 | 200 | 25 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L141.05 H155.00 Last148.39 inside |
| 2026-09-04 | 1d | 140 | 160 | 148 | 158 | 55 | trend-up | elevated | 6.42 | 145.14 | 155.00 | 153.47 | yes | yes | 0.3% | closed | next-session 2026-09-08 official L145.14 H155.00 C153.47 inside 140-160; 1.10x tagged elevated (should be normal) |
| 2026-09-04 | 1w | 135 | 170 | 145 | 165 | 45 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 148.39 |  |  |  | open | Day 4/5; closes after 2026-09-14 RTH; path thru 9/11 intra L144.89 H155.00 Last148.39 inside 135-170 |
| 2026-09-04 | 1m | 120 | 190 | 140 | 175 | 35 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H155.00 Last148.39 inside |
| 2026-09-04 | 3m | 100 | 230 | 130 | 200 | 30 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H155.00 Last148.39 inside |
| 2026-09-08 | 1d | 144 | 160 | 145 | 155 | 40 | digestion | below-avg | -1.20 | 145.55 | 153.00 | 147.55 | yes | yes | 1.6% | closed | next-session 2026-09-09 official RTH (MarketWatch/YCharts/Yahoo) O152.04 H153.00 L145.55 C147.55 Vol~120.59M (~1.44x); H/L/C inside 144-160; C inside bias 145-155; bias mid 150; C vs 9/08 official 153.47 down toward bias; known-event extra-low held |
| 2026-09-08 | 1w | 135 | 175 | 142 | 165 | 40 | digestion | below-avg | -1.20 | 144.89 | 155.00 | 148.39 |  |  |  | open | Day 3/5; closes after 2026-09-15 RTH; path thru 9/11 intra L144.89 H155.00 Last148.39 |
| 2026-09-08 | 1m | 120 | 195 | 135 | 180 | 30 | digestion | below-avg | -1.20 | 144.89 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H155.00 Last148.39 |
| 2026-09-08 | 3m | 100 | 240 | 125 | 210 | 25 | digestion | below-avg | -1.20 | 144.89 | 155.00 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H155.00 Last148.39 |
| 2026-09-09 | 1d | 139 | 161 | 144 | 156 | 45 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.18 | yes | yes | 1.2% | closed | next-session 2026-09-10 official RTH O145.00 H154.70 L144.89 C148.18 Vol~118.60M; H/L/C inside 139-161; C inside bias 144-156; bias mid 150; live-impulse −4.81% vs 153.47 should have been trend-down |
| 2026-09-09 | 1w | 130 | 175 | 140 | 165 | 40 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.39 |  |  |  | open | Day 2/5; closes after 2026-09-16 RTH; path thru 9/11 intra L144.89 H154.70 Last148.39 |
| 2026-09-09 | 1m | 115 | 195 | 130 | 180 | 30 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H154.70 Last148.39 |
| 2026-09-09 | 3m | 95 | 240 | 120 | 210 | 25 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H154.70 Last148.39 |
| 2026-09-10 | 1d | 136 | 162 | 145 | 155 | 45 | digestion | elevated | -3.86 | 145.92 | 150.59 | 148.39 |  |  |  | preliminary | next-session 2026-09-11 RTH; Yahoo ~12:11 ET intra L145.92 H150.59 Last148.39 inside 136-162; official close pending |
| 2026-09-10 | 1w | 128 | 180 | 140 | 165 | 40 | digestion | elevated | -3.86 | 144.89 | 154.70 | 148.39 |  |  |  | open | Day 1/5; closes after 2026-09-17 RTH; path thru 9/11 intra L144.89 H154.70 Last148.39 |
| 2026-09-10 | 1m | 115 | 200 | 130 | 180 | 30 | digestion | elevated | -3.86 | 144.89 | 154.70 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H154.70 Last148.39 |
| 2026-09-10 | 3m | 95 | 245 | 120 | 210 | 25 | digestion | elevated | -3.86 | 144.89 | 154.70 | 148.39 |  |  |  | open | path thru 9/11 intra L144.89 H154.70 Last148.39 |
| 2026-09-11 | 1d | 136 | 164 | 142 | 156 | 45 | digestion | elevated | 0.43 |  |  |  |  |  |  | open | next-session 2026-09-14 RTH; recovered from 9/11 Analysis email; Analysis SHA-reuse fail (emitted pre-write 6e4d34f3) |
| 2026-09-11 | 1w | 128 | 182 | 138 | 168 | 40 | digestion | elevated | 0.43 | 145.92 | 150.59 | 148.39 |  |  |  | open | Day 0/5; closes after 2026-09-18 RTH; recovered from 9/11 Analysis email; path thru 9/11 intra L145.92 H150.59 Last148.39 |
| 2026-09-11 | 1m | 115 | 205 | 130 | 185 | 30 | digestion | elevated | 0.43 | 145.92 | 150.59 | 148.39 |  |  |  | open | residual unlock 9/24 + F14; recovered from 9/11 Analysis email; path thru 9/11 intra L145.92 H150.59 Last148.39 |
| 2026-09-11 | 3m | 95 | 250 | 120 | 215 | 25 | digestion | elevated | 0.43 | 145.92 | 150.59 | 148.39 |  |  |  | open | Q3 earnings unlock ~Nov; recovered from 9/11 Analysis email; path thru 9/11 intra L145.92 H150.59 Last148.39 |
