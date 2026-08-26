# Macro Theme Tracker

One row per `(analysis_date, theme_id, proxy)`. Update in place. Do not duplicate.

**Status:** `open` · `preliminary` · `closed` · `expired` · `falsified`  
**Hit (direction):** proxy total return over `horizon_days` moved in the predicted direction.  
**Hit (range):** realized % change fell inside `[pct_low, pct_high]` (inclusive).  
**Range hit** is the primary grade; direction is secondary.

Horizons are calendar days from `analysis_date` (not trading sessions). Grade at horizon end ±1 trading day OK.

| analysis_date | theme_id | theme | side | industry | proxy | horizon_days | pct_low | pct_high | conf | falsifier | action | actual_pct | hit_range | hit_dir | status | graded_date | notes |
|---------------|----------|-------|------|----------|-------|--------------|---------|----------|------|-----------|--------|------------|-----------|---------|--------|-------------|-------|
| (seed) | | | | | | | | | | | | | | | open | | Tracker seeded 2026-08-26; first Analysis run replaces seed |
