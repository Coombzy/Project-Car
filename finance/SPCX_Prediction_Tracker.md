# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-10-12 official:** Auditor 10/11 closed through 10/09 including 10/02 1d MISS upper, 10/03 1d MISS upper, 10/04 1d MISS upper, 9/28 1w HIT, 9/29 1w MISS upper, 9/30 1w MISS upper, 10/01 1w MISS upper, 10/02 1w HIT, 9/03 1m HIT. Do not reopen. Widen-high ON (last 3 closed 1w upper-exceed). ATR-proxy last-5 median $5.77. Stacked floors: 1d/1w high >=185.08, low <=154.84. 1d width >=2.5x ATR, 1w >=4.0x ATR.

**1m Day N/21:** Oldest open 1m after Auditor 10/11 closes: next after 9/03.

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-10-12** O **$164.66** H **$167.07** L **$160.85** C **$163.42** Vol ~67.4M (+0.52% vs 10/09 C$162.57). Path high **$176.42** (10/06) for open rows whose window includes it. Path low recent **$158.62** (10/05). Last-5 H-L approx 13.85/5.03/5.66/7.60/5.77 median **$5.77**. Rel Vol ~normal. prior_day_pct **+1.25** (as of 10/09; 10/12 +0.52). Regime digestion. Prompt wrapper v1.33 rules. **Write-streak: 0**. Daily 10/13 insert. Bias midpoint above C162.57. Hard-fail if 1d high parked on 176/180/185 without clearance.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next 8/27 inside |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 145.23 | 140.71 | yes | yes | 3.6% | closed | Day 5/5 after 9/02 |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 158.13 | 148.68 | yes | yes | 2.5% | closed | Day 21/21 after 9/25 official; path L135.10 H158.13 C148.68 inside 110-175 |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 159.84 | 158.96 |  |  |  | open | path L135.10 H159.84 Last158.96; unlock 10/09 + 10/24; Q3 ~Nov + Dec-8 remainder |
| 2026-10-13 | 1d | 154 | 186 | 163 | 172 | 45 | digestion | normal | 1.25 |  |  |  |  |  |  | open | next RTH; ATR $5.77; width 32>=2.5x; high 186 clears 185.08; low 154<=154.84; bias mid 167.5>162.57; widen-high ON |
| 2026-10-13 | 1w | 150 | 192 | 160 | 175 | 40 | digestion | normal | 1.25 | 160.85 | 167.07 | 163.42 |  |  |  | open | Day 0/5; width 42>=4.0x; high clears 185.08+; bias mid 167.5>162.57; path as-of 10/12 |
| 2026-10-13 | 1m | 140 | 210 | 155 | 185 | 32 | digestion | normal | 1.25 | 160.85 | 167.07 | 163.42 |  |  |  | open | path as-of 10/12 L160.85 H167.07 C163.42 |
| 2026-10-13 | 3m | 120 | 250 | 140 | 200 | 26 | digestion | normal | 1.25 | 160.85 | 167.07 | 163.42 |  |  |  | open | path as-of 10/12; longer horizon |