# SPCX Daily Analysis Prompt

**Version:** 1.24  
**Last edited:** 2026-09-25T14:10:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first. After the table: `get_file_contents` tracker → `create_or_update_file` today's 4 rows + path refresh. Dual-write with `push_files` if SHA unchanged. TRACKER_SHA must differ from pre-write SHA. Email is not a write. Never push a header-only tracker or prompt. Outbound tracker ≥ inbound row count and ≥64 data rows.
3. If today's 4 rows already exist: PREEXISTING_ROWS + current blob SHA. Do not duplicate 9/22, 9/23, or 9/24 rows. Do not rewrite locked 9/14, 9/16, 9/18, 9/22, 9/23, 9/24.
4. Anti-wipe: outbound tracker ≥ inbound row count and ≥64 data rows. Never header-only. Streak 0. Daily inserts session-day rows; Auditor grades/path-refreshes/closes only.
5. Restore a stub prompt (<2kB / missing Process rules) to this v1.24 body before using it. Restore a header-only / <60-row tracker from commit `3afe8900814f026f09f7dfd57c479a7a311626f9` / blob `d0afc402b6d082e8f1fe071ed83423c13f8b5d62` before writing.

## Range / regime

- ATR-proxy: last-5 TR median vs 14d mean TR; if they differ <20%, use the last-5 median.
- 1d width ≥2.0× ATR; 1w ≥3.0× (≥4.0× only if last 5 sessions include ≥+5%).
- Never park 1d/1w high on $149 / $150 / $155.
- After each official EOD, recompute printed extremes then restack +1.0× ATR on 1d/1w. Hard-fail reprint if short.
- Keep known-event extra while the next dated unlock sits inside the next 10 RTH.
- pred_rel_vol vs 20d official volume only. prior_day_pct from last official close. Do not bucket Rel Vol off mid-session volume.
- Regime from last official close location / impulse, not live mid-prints.
- 1d maps to the next RTH. Do not close 1w mid-session; Auditor marks Day N/5 closes.

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward 1d/1w/1m/3m; 3-bullet decision map; disclaimer. Self-check including stacked floors + hard-fail reprint yes/no + anti-wipe ≥64.
