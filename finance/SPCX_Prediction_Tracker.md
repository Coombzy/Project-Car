# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` · `closed` · `expired`  
Hit: actual H/L/Close (or path high/low over the horizon) stayed inside **range** (not only bias).

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| (seed) | | | | | | | | | | | | | | | | open | Tracker seeded 2026-08-26; first Analysis run appends real rows |
