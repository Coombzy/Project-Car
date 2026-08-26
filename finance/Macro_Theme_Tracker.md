# Macro Theme Tracker

One row per `(analysis_date, theme_id, proxy)`. Update in place. Do not duplicate.

**Status:** `open` · `preliminary` · `closed` · `expired` · `falsified`  
**Hit (direction):** proxy total return over `horizon_days` moved in the predicted direction.  
**Hit (range):** realized % change fell inside `[pct_low, pct_high]` (inclusive).  
**Range hit** is the primary grade; direction is secondary.

Horizons are calendar days from `analysis_date` (not trading sessions). Grade at horizon end ±1 trading day OK.

| analysis_date | theme_id | theme | side | industry | proxy | horizon_days | pct_low | pct_high | conf | falsifier | action | actual_pct | hit_range | hit_dir | status | graded_date | notes |
|---------------|----------|-------|------|----------|-------|--------------|---------|----------|------|-----------|--------|------------|-----------|---------|--------|-------------|-------|
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz temporary corridor progress eases oil risk premium | benefit | Airlines | JETS | 30 | 4 | 15 | 55 | Renewed kinetic escalation or corridor fails; Brent >95 | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz temporary corridor progress eases oil risk premium | hurt | Upstream Energy | XLE | 30 | -12 | -2 | 60 | Renewed kinetic escalation or corridor fails; Brent >95 | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz temporary corridor progress eases oil risk premium | hurt | Oil | USO | 30 | -15 | -3 | 55 | Renewed kinetic escalation or corridor fails; Brent >95 | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-us-canada-tariffs | Escalating US-Canada mutual 50% tariffs fragment NA supply chains | hurt | Canada Equities | EWC | 60 | -10 | -1 | 50 | Rapid de-escalation / new USMCA deal | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-us-canada-tariffs | Escalating US-Canada mutual 50% tariffs fragment NA supply chains | benefit | Mexico Equities | EWW | 60 | 2 | 12 | 45 | Rapid de-escalation / new USMCA deal | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-us-canada-tariffs | Escalating US-Canada mutual 50% tariffs fragment NA supply chains | hurt | Autos | CARZ | 60 | -12 | -2 | 50 | Rapid de-escalation / new USMCA deal | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-treasury-fed-tension | Treasury long-bond buybacks collide with Fed inflation fight | benefit | Long Duration Bonds | TLT | 45 | 2 | 10 | 50 | Buybacks halted or yields spike on fiscal news | watch |  |  |  | open |  |  |
| 2026-08-26 | 20260826-treasury-fed-tension | Treasury long-bond buybacks collide with Fed inflation fight | hurt | Financials | XLF | 45 | -8 | 0 | 45 | Buybacks halted or yields spike on fiscal news | watch |  |  |  | open |  |  |
