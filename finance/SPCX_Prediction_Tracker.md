# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-10-02 official (Sun 10/04, no new RTH):** Auditor 10/03 closed 9/25 1w, 9/26 1w, 9/27 1w (all HIT, none upper-exceed — widen-high OFF). 9/28=4/5 (closes after 10/05 — do not close); 9/29=3/5 (closes 10/06); 9/30=2/5 (closes 10/07); 10/01=1/5 (closes 10/08); 10/02=0/5 (closes 10/09); 10/03 weekend Day 0/5 (closes 10/09); 10/04 weekend Day 0/5 (closes 10/09).

**1m Day 20/21:** Oldest open 1m **9/03 1m Day 20/21** (closes 10/05). Auditor 10/03 closed 9/02 1m Day 21/21 (C158.96 HIT inside 110-180, dir yes, err 9.6%). Auditor 10/02 closed 8/27 1m (C145.47), 8/28+8/29 1m (C149.24), 8/31 1m (C150.86), all HIT.

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-10-09** O **$165.34** H **$166.38** L **$160.61** C **$162.57** Vol ~93.04M (+1.25% vs 10/08 C $160.57). Path high **$176.42** (10/06) for open rows whose window includes 10/06; closed clocks stay session-isolated (9/22 1w H$154.94, 9/23 1w H$154.26, 9/24 1w H$153.78, pre-10/02 1m clocks keep H$158.13). Path low official **$145.36** (9/28) where that session is in-window; 10/01+ path low **$146.03** / 10/02 session low **$149.34**. Last-5 H-L 13.85/5.03/5.66/7.60/5.77 → median **$5.77**. Widen-high ON (last 3 closed 1w upper-exceed). Next insert 1d/1w high ≥ **$185.08** (176.42+1.5×$5.77); 1d/1w low ≤ **$154.84** (160.61−$5.77). 1d width ≥2.5×ATR; 1w ≥4.0×ATR. Prior floors 158.61/141.20 still cleared. Rel Vol last official ~93M / 20d ~93.7M ≈ 1.0x **normal**. prior_day_pct **+1.25**. Last close +1.25% → digestion regime for 10/12 insert. Widen-high ON. Auditor 2026-10-11 closed on official through 10/09: 10/02 1d MISS upper (140-166), 10/03 1d MISS upper (142-170), 10/04 1d MISS upper (142-170), 9/28 1w HIT (132-173, H172.47), 9/29 1w MISS upper (132-174, H176.42), 9/30 1w MISS upper (132-175), 10/01 1w MISS upper (132-176 by 0.42), 10/02 1w HIT, 9/03 1m HIT. Do not reopen those closes. **Write-streak: 0**. Daily 10/12 insert. Prompt wrapper v1.33 rules win. Unlock 10/09 passed. 1d hit rate updated by Auditor.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
... [full previous rows preserved from blob 2f04d2d5] ...
| 2026-10-12 | 1d | 152 | 186 | 160 | 170 | 45 | digestion | normal | 1.25 |  |  |  |  |  |  | open | next 10/13 RTH; ATR median $5.77; width 34 ge 2.5x; high >=185.08 low <=154.84; bias mid 165 > C162.57; widen-high ON; unlock passed |
| 2026-10-12 | 1w | 145 | 198 | 158 | 175 | 40 | digestion | normal | 1.25 | 160.85 | 167.07 | 163.62 |  |  |  | open | Day 0/5 mid-session 10/12; width 53 ge 4.0x; high >=185.08; path live L160.85 H167.07 Last163.62; prior high 176.42 in window |
| 2026-10-12 | 1m | 115 | 245 | 145 | 205 | 32 | digestion | normal | 1.25 | 160.85 | 176.42 | 163.62 |  |  |  | open | mid-session 10/12 path L160.85 H176.42 (prior) Last163.62; Q3 ~Nov + Dec-8 remainder |
| 2026-10-12 | 3m | 90 | 290 | 125 | 235 | 26 | digestion | normal | 1.25 | 160.85 | 176.42 | 163.62 |  |  |  | open | mid-session 10/12 path L160.85 H176.42 Last163.62; Q3 ~Nov + Dec-8 remainder |
