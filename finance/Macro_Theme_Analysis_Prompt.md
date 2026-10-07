# Macro Industry Theme Map — Analysis Prompt

**Version:** 1.6 (2026-10-06)  
**Last edited:** 2026-10-07 00:50 UTC  
**Supersedes:** v1.5 (expiry clears the tell, pre-haircut floor, shadow block)  
**v1.6 user edit:** the diesel-plays answer skipped the contract and waived already-priced for a 52-week high. Ad-hoc replies are now bound. Overlay is a row. PLACEHOLDER is replaced once.  
**Location:** `Project-Car/finance/`

Read `finance/Macro_WRITE_RULES.md` and `finance/Macro_README.md` first. Not financial advice. Selection support only — no position sizes.

## Goal

Turn the last ~72h of macro / policy / geopolitical news into **at most 3 themes**, each with industry beneficiaries AND hurt side, liquid proxies **and up to 3 single-stock picks**, **horizon_days**, **% change range**, falsifier, and action. Persist the write-up in the log and append tracker rows for grading.

**Priority:** if more than 3 durable candidates exist, keep the 3 with the **highest potential upside %** and the **highest chance of seeing it**. Score each candidate as `(conf / 100) × pct_high` of its best *benefit* name. Label that score **expected upside points**, not a probability. State the pre-haircut and post-haircut scores. Do not pick a high-upside / low-conf lottery over a medium-upside / higher-conf theme.

Score floor is **pre-haircut**. If the best benefit score is under **5** before any priced-in haircut, do not book that candidate. A haircut changes `action` to `watch` or `ignore`. It does not delete a name that cleared 5. If nothing durable, output **0–1** themes and say so — do not invent. A 0-theme result is still an official run and must be logged.

## Hard rules

1. Max **3** new `theme_id`s. An inverse still inside the parent horizon is **one overlay row** (`notes` starts with `overlay`), parent ranges frozen, and it does not count toward the cap. A prose note with zero rows cannot be graded.
2. Skip celebrity noise, single-name *earnings-only* stories, empty "AI changes everything."
3. **Prefer single stocks with high potential for large % changes.** Names must still be **liquid enough to grade** (primary listing NYSE / Nasdaq / TSX; no OTC/pinks; skip thin story stocks). ETFs remain OK as *hurt-side baskets* or when no clean liquid name exists. Do not widen the venue list to force a country story.
4. Every proxy **and every stock pick** MUST have: `horizon_days` ∈ {14, 30, 60, 90}, `pct_low`, `pct_high`, `conf` (40–85), `spot_at_call`, `due_date`, proxy-specific `falsifier`. Do **not** use 45 on new rows. Do not rewrite frozen 45-day rows.
5. % ranges = expected **total return %** over `horizon_days`. Widen when uncertain; do not fake tight precision.
6. Benefit side → range bias above 0; hurt → bias below 0 when conviction exists.
7. `theme_id` format: `YYYYMMDD-slug`
8. `action`: `watch` | `deep-dive` | `ignore`. **At most one `deep-dive` per run.** Default `watch`. Use `ignore` when the move is already priced.
9. **Do not change** ranges/horizons on already-open tracker rows, including illegal 45-day rows. New idea = new row. Status may change (`open` → `expired-ungraded` or graded). Ranges may not.
10. Per theme: **suggest up to 3 best stocks**. Same cash-flow line = one ticker. Fewer than 3 with an explicit screen fail is success. Do not add a name to fill the slot. If a pick is also a proxy, **one tracker row**.
11. **No tickers until the industry is done** for any kept theme. If zero themes are kept, still write a **shadow industry block** for the top dropped candidate, labeled `not booked`, and do not append tracker rows for it.
12. **Expiry clears the tell.** List open rows with `due_date` < analysis_date. Grade in place if a price is in hand. If not, set `status=expired-ungraded` in the same PR and do not touch ranges. After that flag, a flipped tell **may** be a new `theme_id`. An inverse is an overlay row only while the old row is still inside its horizon (`due_date` >= analysis_date). Chat-only "not edited" is a process miss.
13. If `main` already has a v1.4+ log header for today, or an open PR for that `analysis_date`, do not start a second official run. A branch-only entry with no open PR is not an official entry. A 0-theme entry counts as that header once it is on `main` or in an open PR.
14. First line of every official run, and of every chat answer that uses these gates, must cite **Version, ref, and blob SHA actually read**. Do not cite a version you did not re-fetch.
15. **Two clocks are not one trade.** If one tell has a near-term slug and a residual horizon, each name gets one horizon. State which clock the name is on. Do not present a 14-day cost relief and a 60-day residual long as the same expression.
16. **Empty tracker is not a screen.** A name at a 52-week high on this tell fails already-priced even if no tracker row exists. The ~150% YTD rule is an extra cut, not the only one.

## Ad-hoc selection answers

If the user asks for the plays, the names, or the best expression and does not ask to book a run:

- Do not append tracker rows and do not prepend the log.
- Still apply the gates. First line: `Prompt vX.Y | ref | blob <sha> | not booked`.
- For each name: tell, one source URL, already-priced check (52-week high and YTD or 12-month move), one horizon in {14, 30, 60, 90}, one numeric falsifier.
- One name per cash-flow line. State the sign of any offset (a fuel-export halt supports the crack; a stock release hurts it).
- Label the print. NYMEX ULSD futures is not AAA retail diesel. An inventory **level** needs the EIA weekly table URL. A portal draw is not a stock level. If two sources differ by more than 2%, quote both. Do not average.

## Industry analysis (required, before any stock picks)

For **each** kept theme, research the affected industry. Write the block in the log **above** the stocks. If none kept, write the same block once for the top drop and mark it `not booked`.

1. **Value chain** — who collects the cash.
2. **Transmission** — how the 72h news hits this industry. Name the **tell**. If the tell moved the wrong way in the 72h window, action = `ignore` and do not book that direction.
3. **Peer universe** — 5–8 liquid names plus the ETF. One line each: leverage, last print, 52-week high or not, rough YTD or 12-month move.
4. **Screen** — why these names win. Same cash-flow line = one ticker. Do not force 3. "Not an open row" is not a reason to pick.
5. **Hurt side** — who loses in the same chain.
6. **Already priced?** — a 52-week high on this tell fails unless the range is widened and confidence is cut, and action cannot be `deep-dive`. Also show the haircut: `residual_pct_high = pct_high × (1 − f)`, where `f` is the fraction of the thesis the tell has already moved. Worked example: 52 × 12 = 6.2, eligible; f = 0.5 → residual pct_high 6, post score 3.1, action `watch`, not a drop. A name up more than ~150% over 12 months on this tell is already priced on the same terms.

Only after 1–6, output stocks with ranges for kept themes.

## Proxy / pick quality

- **No duplicate beta.** One expression per cash-flow line (name or ETF, not both).
- **Match the barrel / region.** Label the print: NYMEX ULSD futures is not AAA retail diesel. Brent is not WCS–WTI.
- **spot_at_call:** equity last print and the tell, plus source URL and timestamp. If two sources differ by more than 2%, quote both and widen or drop. Do not silently average.
- An inventory level requires the EIA Weekly Petroleum Status Report table URL. A secondary portal figure is not the level.
- Falsifier must be a number checkable before `due_date`. No "confidence returns."
- `due_date` = analysis_date + horizon_days.
- Tracker `notes` starts with `pick`, `basket`, or `overlay`. `source_note` must include a URL.

## Overlap / stack scan (required)

Check every pair and every candidate against open tracker rows. Same cash-flow line, duty vs political tail, sign if one falsifies. Material stack = overlay row on the primary theme, not a 4th id.

Inverse rule: one overlay row if the prior row is still inside its horizon. If `due_date` < analysis_date, expire it first, then the flip can be a new id. Do not let an ungraded backlog silence the only live catalyst.

Energy exemption check stays: Section 338 50% list excludes energy, potash, fish, critical minerals. Oil + Canada tell is WCS–WTI, not Brent alone.

## Required steps (in order)

1. Read WRITE_RULES + this file + newest log + all open tracker rows + last 5 closed. Refetch log raw if PLACEHOLDER, under ~500 chars, or no `###` header. Record Version, ref, blob SHA.
2. List past-due open rows. Grade or mark `expired-ungraded` in the same PR. Do not edit ranges. Chat-only is a fail.
3. Collect ~72h news. Cite URLs. Record driver spots with source and timestamp. Label futures vs retail. Inventory levels need the EIA table URL.
4. Draft themes. Overlap scan including open rows, after the expiry pass. No stock names yet.
5. Industry analysis before any ticker. Shadow block if zero kept. Apply the 52-week-high screen.
6. Pick ≤3 stocks. One horizon per name. Score expected upside points **pre-haircut**. Drop only if pre-haircut < 5. Show haircut arithmetic; it sets action. Horizons in {14,30,60,90}. At most one deep-dive.
7. Self-check: industry block above picks (or shadow if zero), no duplicate beta, numeric falsifier, URL on every print, 52-week check done, energy exemption if needed.
8. Commit log first, including a 0-theme entry. If the log body is still `PLACEHOLDER` after the refetch, replace the stub once. Do not prepend onto PLACEHOLDER. SHA immediately before write. Ruleset 409 → one branch, log + tracker status edits, then PR. Retry-once is SHA conflict only.
9. Append tracker rows for booked names and for overlay rows. Status-only edits on past-due rows are allowed in that same commit. SHA immediately before write.
10. Report SHA or PR URL, blob cited, and `rows appended: N`. `0` is valid. Do not claim a drafted tracker as committed.

## Output structure (chat + log)

First line: `Prompt vX.Y | ref | blob <sha>`

**Key Takeaway**

**Driver snapshot** (even on a 0-theme day; futures vs retail labeled; inventory level only with EIA URL)

**Past-due actions** (status written, or "none past due")

**Overlap scan**

**Ranking** (pre-haircut and post-haircut expected upside points; kept / dropped / overlay)

For each kept theme: theme_id, title, mechanism, horizon_days per name, beneficiaries/hurt, **industry analysis before stocks**, then up to 3 stocks, proxies table, numeric falsifier, action.

If none kept: one shadow industry block, labeled `not booked`.

Then calibration line + disclaimer.

Ad-hoc answers use the short form in **Ad-hoc selection answers** and say `not booked`.

## Tracker row contract

Columns: `analysis_date, theme_id, theme, side, industry, proxy, horizon_days, pct_low, pct_high, conf, falsifier, action, spot_at_call, due_date, source_note, actual_pct, hit_range, hit_dir, status, graded_date, notes`

Fill first 15 at analysis; `status=open`. Allowed later status: `closed`, `falsified`, `expired-ungraded`. `source_note` includes a URL. `notes` starts with `pick`, `basket`, or `overlay`.

## Success criteria

- [ ] WRITE_RULES followed (SHA, log gate, no range edits)
- [ ] Version, ref, and blob SHA cited from the file just read
- [ ] ≤3 new theme_ids; scores labeled expected upside points, pre-haircut; haircut shown
- [ ] Industry analysis before any ticker, or a shadow block if zero kept
- [ ] 52-week high on this tell fails already-priced even if the tracker is empty
- [ ] One horizon per name when two clocks share a tell
- [ ] Past-due rows graded or `expired-ungraded` in the same PR, not chat-only
- [ ] Inverse inside an open horizon is one overlay row, not a prose note
- [ ] A 0-theme day is logged; PLACEHOLDER stub replaced once, not prepended
- [ ] Ad-hoc play answers use the short form and do not book
- [ ] No duplicate beta; numeric falsifier; equity + tell + URL in spot/source; EIA URL for a stock level
- [ ] ≤1 deep-dive; commit SHA or PR URL; rows appended count
