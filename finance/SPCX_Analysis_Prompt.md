# SPCX Daily Analysis Prompt

**Version:** 1.35  
**Last edited:** 2026-10-07T16:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Process (hard gates)

1. First ~20 lines of the Daily output MUST be Key Takeaway + parseable 4-row table (`horizon, range_low, range_high, bias_low, bias_high, conf, pred_regime, pred_rel_vol, prior_day_pct`).
2. Write-first. After the table: get_file_contents tracker, then write today's 4 rows + path refresh with the full table body. Prefer push_files. TRACKER_SHA must differ from pre-write SHA. Email is not a write. Never push a header-only tracker, TRACKER_BODY, PLACEHOLDER, SEE_FILE, or prompt stub. Outbound tracker >= inbound row count and >=64 data rows and >=15kB.
3. If today's 4 rows already exist: PREEXISTING_ROWS + current blob SHA. Do not duplicate 9/22 through 10/04 rows. Do not rewrite locked bands. Do not reopen Auditor 10/07 closes (10/02 1d, 10/03 1d, 10/04 1d, 9/28 1w, 9/29 1w, 9/03 1m, 9/04 1m). Do not backfill invented 10/05 or 10/06 bands.
4. Anti-wipe: outbound >= inbound and >=64 `| 2026-` rows and >=15kB. 18 pipe fields per row. Hard-fail if status lands in pct_error.
5. Restore a stub prompt to this v1.35 body. Abort SHAs: daf3296c, b3815b67, 547fe344. Do not treat blob 2f04d2d51787b38b2f784214d9ce6cbb6208427d (120 rows) as a stub.

## Range / regime

- ATR-proxy: last-5 TR median vs 14d mean TR; if they differ <20%, use the last-5 median. After 10/06 official: last-5 H-L 5.03/13.85/10.50/7.75/4.83 median $7.75. Do not reuse the 10/02 $5.44 figure.
- 1d width >=2.0x ATR; 1w >=3.0x (>=4.0x if last 5 sessions include >=+5%). 10/05 close was +7.63%, so 1w width stays >=4.0x ATR while that print is inside the open 1w window (through 10/09).
- Impulse-continuation gate ON: last 2 official closes include >=+5% OR that session H-L >=1.5x prior ATR, OR 2+ of the last 3 closed 1d are upper-exceed. Next 1d range_high >= session high + 2.5x current ATR-proxy. After 10/06: 1d/1w high >= $195.80 (176.42+2.5x7.75); 1d/1w low <= $150.87 (158.62-1.0x7.75). 1d width >=3.0x ATR under this gate. Hard-fail if a new 1d high is parked on 166/168/170/172/175/176/180/185/190. Gate stays on even though 10/06 close was only +0.49%.
- Never park 1d/1w high on 149/150/155/156/157/159/160/166/170/172/176. Closed 1d misses: 9/02, 9/14, 9/16, 10/02 H172.47>166, 10/03 H172.47>170, 10/04 H172.47>170. 1d hit rate after 10/07 audit: 24/30.
- Keep known-event extra while unlock 2026-10-09 sits inside the next 10 RTH.
- pred_rel_vol vs 20d official volume only. After 10/06: Rel Vol ~107.0M / 20d ~96M ~ 1.11x elevated; prior_day_pct +0.49.
- Regime: a >=+5% session still inside the open 1w window means trend-up. 10/06 +0.49% does not cancel 10/05 +7.63%. Do not relabel locked 10/02 digestion rows.
- Bias midpoint must sit above C171.92. 10/02 1d bias mid $156 sat below session close $158.96 and finished at $171.09.
- 1d maps to the next RTH. 10/07 mid-session is not a close. Do not close 9/30 1w before 10/07 RTH.
- Last 3 closed 1w (9/27 HIT, 9/28 HIT not upper-exceed gap 0.53, 9/29 MISS upper): widen-high 2-of-3 OFF. Impulse-continuation 2.5x ON.

## Path + close-clock (v1.35)

- Path H/L/C from that analysis_date session through last official or horizon close. 10/03 and 10/04 path is 10/05-10/06 L158.62 H176.42 C171.92. Closed clocks stay session-isolated (9/28 1w and 9/03 1m stop at 10/05 H172.47; 9/29 1w and 9/04 1m include 10/06 H176.42).
- Auditor closed 2026-10-07: 10/02 1d MISS upper dir no err 9.7%; 10/03 1d MISS upper dir yes err 6.6%; 10/04 1d MISS upper dir yes err 5.6%; 9/28 1w HIT not upper-exceed; 9/29 1w MISS upper dir no err 17.8%; 9/03 1m HIT err 10.4%; 9/04 1m HIT err 9.2%. Oldest open 1m: 9/08 Day 20/21 (closes 10/07).

## Report order

Key Takeaway; 4-row table; TRACKER_SHA; snapshot; technical; news; forward 1d/1w/1m/3m; 3-bullet decision map; disclaimer. Self-check floors 195.80/150.87 + bias mid above C171.92 + impulse gate on.
