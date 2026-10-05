# Macro Industry Theme Map — Analysis Prompt

**Version:** 1.4 (2026-10-05)  
**Last edited:** 2026-10-05 14:35 UTC  
**Supersedes:** v1.3 (industry analysis before any ticker)  
**v1.4 user edit:** log gate, ruleset write path, grade-before-new-theme, score units, one name per cash-flow line, numeric falsifier.  
**Location:** `Project-Car/finance/`

Read `finance/Macro_WRITE_RULES.md` and `finance/Macro_README.md` first. Not financial advice. Selection support only — no position sizes.

## Goal

Turn the last ~72h of macro / policy / geopolitical news into **at most 3 themes**, each with industry beneficiaries AND hurt side, liquid proxies **and up to 3 single-stock picks**, **horizon_days**, **% change range**, falsifier, and action. Persist the write-up in the log and append tracker rows for grading.

**Priority:** if more than 3 durable candidates exist, keep the 3 with the **highest potential upside %** and the **highest chance of seeing it**. Score each candidate as `(conf / 100) × pct_high` of its best *benefit* name. Label that score **expected upside points**, not a probability. State the score in the log. Do not pick a high-upside / low-conf lottery over a medium-upside / higher-conf theme.

If the best benefit score is under **5** after a priced-in haircut, book **0** themes. If nothing durable, output **0–1** themes and say so — do not invent.

## Hard rules

1. Max **3** themes. Overlaps are **overlay proxies or notes**, not a 4th `theme_id`.
2. Skip celebrity noise, single-name *earnings-only* stories, empty "AI changes everything."
3. **Prefer single stocks with high potential for large % changes.** Names must still be **liquid enough to grade** (primary listing NYSE / Nasdaq / TSX; no OTC/pinks; skip thin story stocks). ETFs remain OK as *hurt-side baskets* or when no clean liquid name exists.
4. Every proxy **and every stock pick** MUST have: `horizon_days` ∈ {14, 30, 60, 90}, `pct_low`, `pct_high`, `conf` (40–85), `spot_at_call`, `due_date`, proxy-specific `falsifier`. (v1.1 banned 14 — v1.2 restores it to match Macro Alpha. Do **not** use 45 on new rows. Do not rewrite frozen 45-day rows.)
5. % ranges = expected **total return %** over `horizon_days`. Widen when uncertain; do not fake tight precision.
6. Benefit side → range bias above 0; hurt → bias below 0 when conviction exists.
7. `theme_id` format: `YYYYMMDD-slug`
8. `action`: `watch` | `deep-dive` | `ignore`. **At most one `deep-dive` per run.** Default `watch`. Use `ignore` when the move is already priced.
9. **Do not change** ranges/horizons on already-open tracker rows, including illegal 45-day rows. New idea = new row.
10. Per theme: **suggest up to 3 best stocks** (usually benefit-side convexity; 1 of 3 may be the cleanest hurt-side name). Same cash-flow line = one ticker. Fewer than 3 with an explicit screen fail is success. Do not add a name to fill the slot. If a pick is also a proxy, **one tracker row** — do not duplicate.
11. **No tickers until the industry is done.** For each kept theme, complete the **Industry analysis** block (below) *before* listing any stock. Picks must be the output of that analysis, not the starting point.
12. **Grade before a new theme on the same tell.** List open rows with `due_date` <= today. Grade in place if a price is in hand. If not, set `status=expired-ungraded` and do not touch ranges. Do not open a new `theme_id` on that tell until the old row is graded or marked `expired-ungraded`. An inverse of an open row is an overlay note, not a new id, unless the tell has flipped and the old row is flagged ungraded.
13. If today already has a v1.3+ log header, or an open PR for that `analysis_date`, do not start a second official run.

## Industry analysis (required, before any stock picks)

For **each** kept theme, research the affected industry. Write the block in the log **above** the stocks.

1. **Value chain** — who collects the cash.
2. **Transmission** — how the 72h news hits this industry. Name the **tell**. If the tell moved the wrong way in the 72h window, action = `ignore` and do not book.
3. **Peer universe** — 5–8 liquid names plus the ETF. One line each: leverage, last print, rough YTD or 30d move.
4. **Screen** — why these names win. Same cash-flow line = one ticker. Do not force 3.
5. **Hurt side** — who loses in the same chain.
6. **Already priced?** — if the move is in, action = `ignore`. A name up more than ~150% YTD on this tell is already priced unless the range is widened and confidence is cut.

Only after 1–6, output the stocks with ranges.

## Proxy / pick quality

- **No duplicate beta.** One expression per cash-flow line (name or ETF, not both). Two truckers on diesel cost are one test.
- **Match the barrel / region.**
- **spot_at_call:** equity last print and the tell, plus source and timestamp. If two sources differ by more than 2%, widen or drop.
- Falsifier must be a number checkable before `due_date`. No "confidence returns."
- `due_date` = analysis_date + horizon_days.
- Tracker `notes` starts with `pick` or `basket`.

## Overlap / stack scan (required)

Check every pair and every candidate against open tracker rows. Same cash-flow line, duty vs political tail, sign if one falsifies. Material stack = overlay on the primary theme, not a 4th id. Inverse of a still-open row is an overlay note unless that row is graded or `expired-ungraded` and the tell has flipped.

Energy exemption check stays: Section 338 50% list excludes energy, potash, fish, critical minerals. Oil + Canada tell is WCS–WTI, not Brent alone.

## Required steps (in order)

1. Read WRITE_RULES + this file + newest log + all open tracker rows + last 5 closed. Refetch log raw if PLACEHOLDER, under ~500 chars, or no `###` header.
2. List past-due open rows. Grade or mark `expired-ungraded`. Do not edit ranges.
3. Collect ~72h news. Cite sources. Record driver spots with source and timestamp.
4. Draft themes. Overlap scan including open rows. No stock names yet.
5. Industry analysis before any ticker.
6. Pick ≤3 stocks. Score expected upside points. Drop if best score < 5 after priced-in haircut. Horizons in {14,30,60,90}. At most one deep-dive.
7. Self-check: industry block above picks, no duplicate beta, numeric falsifier, energy exemption if needed.
8. Commit log first. SHA immediately before write. Ruleset 409 → one branch, both files, then PR. Retry-once is SHA conflict only.
9. Append tracker rows. SHA immediately before write.
10. Report SHA or PR URL and `rows appended: N`. Do not claim a drafted tracker as committed.

## Output structure (chat + log)

**Key Takeaway**

**Overlap scan**

**Ranking** (expected upside points = conf/100 × pct_high; kept / dropped)

For each theme: theme_id, title, mechanism, horizon_days, beneficiaries/hurt, **industry analysis before stocks**, then up to 3 stocks, proxies table, numeric falsifier, action.

Then calibration line + disclaimer.

## Tracker row contract

Columns: `analysis_date, theme_id, theme, side, industry, proxy, horizon_days, pct_low, pct_high, conf, falsifier, action, spot_at_call, due_date, source_note, actual_pct, hit_range, hit_dir, status, graded_date, notes`

Fill first 15 at analysis; `status=open`. Allowed later status: `closed`, `falsified`, `expired-ungraded`.

## Success criteria

- [ ] WRITE_RULES followed (SHA, log gate, no range edits)
- [ ] Version cited (v1.4+)
- [ ] ≤3 themes; scores labeled expected upside points; overlap includes open rows
- [ ] Industry analysis before any ticker
- [ ] Up to 3 picks, or explicit fail if fewer
- [ ] No duplicate beta; numeric falsifier; equity + tell in spot_at_call
- [ ] Past-due same-tell rows graded or expired-ungraded before a new id
- [ ] ≤1 deep-dive; commit SHA or PR URL; rows appended count
