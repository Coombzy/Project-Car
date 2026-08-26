# Macro Theme Tracker

One row per `(analysis_date, theme_id, proxy)`. Update in place. Do not duplicate.

**Status:** `open` · `preliminary` · `closed` · `expired` · `falsified`  
**Hit (direction):** proxy total return over `horizon_days` moved in the predicted direction.  
**Hit (range):** realized % change fell inside `[pct_low, pct_high]` (inclusive).  
**Range hit** is the primary grade; direction is secondary.

Horizons are calendar days from `analysis_date` (not trading sessions). Grade at `due_date` ±1 trading day.  
**v1.1:** fill `spot_at_call`, `due_date`, `source_note` at prediction time. Do not edit `pct_low`/`pct_high`/`horizon_days` on open rows.

| analysis_date | theme_id | theme | side | industry | proxy | horizon_days | pct_low | pct_high | conf | falsifier | action | spot_at_call | due_date | source_note | actual_pct | hit_range | hit_dir | status | graded_date | notes |
|---------------|----------|-------|------|----------|-------|--------------|---------|----------|------|-----------|--------|--------------|----------|-------------|------------|-----------|---------|--------|-------------|-------|
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz temporary corridor progress eases oil risk premium | benefit | Airlines | JETS | 30 | 4 | 15 | 55 | Renewed kinetic escalation or corridor fails; Brent >95 | watch | Brent 86.8 | 2026-09-25 | FT/Reuters corridor talks |  |  |  | open |  | v1.0 range frozen |
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz temporary corridor progress eases oil risk premium | hurt | Upstream Energy | XLE | 30 | -12 | -2 | 60 | Renewed kinetic escalation or corridor fails; Brent >95 | watch | Brent 86.8 / WTI 80.9 | 2026-09-25 | FT/Reuters corridor talks |  |  |  | open |  | duplicate oil-beta vs USO; v1.1 would drop; range frozen |
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz temporary corridor progress eases oil risk premium | hurt | Oil | USO | 30 | -15 | -3 | 55 | Renewed kinetic escalation or corridor fails; Brent >95 | watch | WTI 80.9 | 2026-09-25 | FT/Reuters corridor talks |  |  |  | open |  | v1.0 range frozen; preferred oil-price proxy |
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz thaw + Gulf heavies back: Alberta WCS stack (overlay) | hurt | Alberta Oil Sands | XEG | 30 | -15 | -3 | 50 | Brent >95 or WCS-WTI narrows with TMX still bid | deep-dive | Brent 86.8; WCS-WTI tell | 2026-09-25 | AER WCS; TMX Asia; energy exempt from 50% |  |  |  | open |  | v1.1 overlay; not a 4th theme; stack with Canada politics not 50% crude duty |
| 2026-08-26 | 20260826-hormuz-thaw | Hormuz thaw + Gulf heavies back: US cokers cheaper heavy (overlay) | benefit | Oil Refiners | CRAK | 30 | 3 | 12 | 50 | Brent >95 / heavy discount collapses | watch | CRAK ~58.7 (26 Aug) | 2026-09-25 | Gulf heavy return; USGC cokers |  |  |  | open |  | v1.1 overlay on Theme 1 |
| 2026-08-26 | 20260826-us-canada-tariffs | Escalating US-Canada mutual 50% tariffs fragment NA supply chains | hurt | Canada Equities | EWC | 60 | -10 | -1 | 50 | Rapid de-escalation / new USMCA deal | watch | NAV n/a | 2026-10-25 | Section 338; energy/potash exempt |  |  |  | open |  | v1.0 frozen; EWC is not Alberta oil (use XEG overlay) |
| 2026-08-26 | 20260826-us-canada-tariffs | Escalating US-Canada mutual 50% tariffs fragment NA supply chains | benefit | Mexico Equities | EWW | 60 | 2 | 12 | 45 | Rapid de-escalation / new USMCA deal | watch | NAV n/a | 2026-10-25 | Section 338 / USMCA |  |  |  | open |  | v1.0 frozen; low-conviction relative |
| 2026-08-26 | 20260826-us-canada-tariffs | Escalating US-Canada mutual 50% tariffs fragment NA supply chains | hurt | Autos | CARZ | 60 | -12 | -2 | 50 | Rapid de-escalation / new USMCA deal | watch | NAV n/a | 2026-10-25 | Section 338 autos/metals |  |  |  | open |  | v1.0 frozen; global mix not NA basket |
| 2026-08-26 | 20260826-treasury-fed-tension | Treasury long-bond buybacks collide with Fed inflation fight | benefit | Long Duration Bonds | TLT | 45 | 2 | 10 | 50 | Buybacks halted or yields spike on fiscal news | watch | long-end squeeze; NAV n/a | 2026-10-10 | Bessent buybacks vs Warsh |  |  |  | open |  | v1.0 45d frozen; v1.1 would use 60 |
| 2026-08-26 | 20260826-treasury-fed-tension | Treasury long-bond buybacks collide with Fed inflation fight | hurt | Financials | XLF | 45 | -8 | 0 | 45 | Buybacks halted or yields spike on fiscal news | watch | NAV n/a | 2026-10-10 | Bessent buybacks vs Warsh |  |  |  | open |  | v1.0 frozen; noisy vs TLT (pct_high=0) |
