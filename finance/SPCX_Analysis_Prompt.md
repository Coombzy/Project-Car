# SPCX Daily Analysis Prompt

**Version:** 1.33  
**Last edited:** 2026-10-05T15:30:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first full tracker. Prefer push_files. Never header-only, PLACEHOLDER, SEE_FILE, or prompt stub. Outbound tracker >= inbound row count and >=64 data rows and >=15kB.
3. Do not duplicate 9/22 through 10/04 rows. Do not rewrite locked bands. Do not reopen Auditor 10/03 closes (9/02 1m, 9/25-9/27 1w, 10/01 1d).
4. Anti-wipe floors above. Daily inserts session-day rows; Auditor grades/closes only. 18 pipe fields per row.
5. Restore a stub prompt to this v1.33 body. Abort SHAs: daf3296c, b3815b67, 547fe344.

## Range / regime

- ATR-proxy after 10/02 official: last-5 H-L median $5.44. Recompute after the next official EOD.
- 1d width >=2.0x ATR; 1w >=3.0x (>=4.0x if last 5 sessions include >=+5%). 10/02 close +7.35% so 1w stays >=4.0x until a new official print. Do not rewrite locked 10/02 (140-166), 10/03 (142-170), 10/04 (142-170) bands.
- Never park 1d/1w high on 149/150/155/156/157/159/160/166/168/170/172. Closed 1d misses: 9/02 H152.30>149, 9/14 L142.87<143, 9/16 H156.87>156. Hit rate 24/27.
- After each official EOD, restack +1.0x ATR on 1d/1w. Floors after 10/02: high >=165.28, low <=143.90.
- Keep known-event extra while 2026-10-09 unlock is inside the next 10 RTH.
- pred_rel_vol vs 20d official volume only. prior_day_pct from last official close. Do not bucket Rel Vol off mid-session volume.
- After a >=+5% official close, next insert bias midpoint must sit above that close.
- Last 3 closed 1w (9/25, 9/26, 9/27) HIT, none upper-exceed. Widen-high OFF.
- Auditor 2026-10-05 mid-session: do not close, do not score. Live 10/05 O158.99 H168.50 L158.62 last ~166.9 vs Fri C158.96. 10/02 1d high 166 already pierced (preliminary). 10/03/10/04 high 170 still contains 168.50.
- Next insert 1d high >= max(live session high, last official high)+1.0x ATR. While 10/09 unlock is inside the next 10 RTH AND the live session is already >=+3% vs prior close, use +1.5x ATR. Floor = 168.50+1.5*5.44 = 176.66 (recompute if official high is higher). Hard-fail if parked on 166/168/170/172.
- Daily runs mid-session (09:00 America/Regina). Do not close 9/03 1m, 9/28 1w, or 10/02/10/03/10/04 1d until 10/05 official close. Do not store live OHLC as 1d actuals.

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward; decision map; disclaimer. Self-check the 176.66 floor (recompute off official high) and anti-wipe.
