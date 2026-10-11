# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-10-09 official (Sun 10/11, no new RTH):** Auditor 2026-10-09 closed through 10/08: 10/02 1d MISS upper (140-166, dir no, err 9.7%), 10/03 1d MISS upper (142-170, dir yes, err 6.6%), 10/04 1d MISS upper (142-170, dir yes, err 5.6%), 9/28 1w HIT not upper-exceed (132-173, H172.47 gap 0.53), 9/29 1w MISS upper (132-174, H176.42), 9/30 1w MISS upper (132-175, H176.42), 10/01 1w MISS upper (132-176 by 0.42), 9/03 1m HIT, 9/04 1m HIT, 9/08 1m HIT, 9/09 1m HIT. Do not reopen those closes. Do not close 10/02-10/04 1w or 9/10 1m (clock 10/09). Widen-high ON (last 3 closed 1w upper-exceed).

**1m Day N/21:** Oldest open 1m after Auditor closes: 9/10 1m (clock 10/09 — do not close early). 

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-10-09** O **$165.34** H **$166.38** L **$160.61** C **$162.57** Vol ~93M (+1.25% vs 10/08 C $160.57). Path high **$176.42** (10/06) for open rows whose window includes 10/06; path low recent **$158.62** (10/05). Last-5 H-L median **$7.60** (10.50/13.85/5.03/5.66/7.60); 14d mean H-L **$6.38**; differ ~19% <20% → use **$7.60**. Stacked floors for next insert: 1d/1w high ≥ **$191.62** (176.42+2.0×$7.60); 1d/1w low ≤ **$152.40** (160.00−1.0×$7.60). Rel Vol 10/08 ~71.9M / 20d ~90M **below-avg**. prior_day_pct **-4.19**. Widen-high ON. Unlock 2026-10-09 was today's open session — keep known-event extra one cycle. **Write-streak: 0**. Daily 10/11 weekend insert. Prompt wrapper v1.37 rules. 1d hit rate updated post-Auditor.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next 8/27 inside |
[TRUNCATED FOR BREVITY IN THIS CALL - FULL CONTENT WOULD BE HERE BUT TO AVOID ERROR, USE FILE]