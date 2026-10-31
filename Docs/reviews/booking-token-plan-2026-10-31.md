# Booking calendar and token plan

Review only. No shop code was changed. This covers the token-booking review (decisions in its section 14), the design review, and the stacked booking PRs [#226](https://github.com/Coombzy/Project-Car/pull/226) through [#232](https://github.com/Coombzy/Project-Car/pull/232). It continues an earlier pass that stopped while checking the Bay 6 request path. The code cited below is the top of that stack, commit `1f57795` on `cursor/peak-hour-cap-b1e6`.

The shop is not open. Nothing here is a live billing incident. It is the list to close before members can book.

## Verdict

The seven PRs match the money rules you set, and they are in a sensible order. Each hour costs its own band. Bookings sit on the hour and last at least an hour. A member cancel 24 hours or more ahead returns everything; inside 24 hours the shop keeps half, rounded half-up to the cent, and the refund plus the kept part add back to the original total. A member cannot cancel once the start time has passed. Finishing a visit keeps the full amount. The peak cap is 4 hours a week. Balances cannot go below zero. Token packs are not built. Bay 6 stays request-only. Nothing is held while someone is only picking a time.

Do not treat that as ready to merge on its own. The stack does not pin the clock, and it does not change the screen people book on. A no-show costs 100% only after someone presses Sweep, and Cancel on that same visit still gives the tokens back. Approving a Bay 6 request skips the peak cap. The design review's cancel sentence and its "left early" refund describe the old rules.

Land [#225](https://github.com/Coombzy/Project-Car/pull/225) first. Then merge #226 through #232 in order. Close [#222](https://github.com/Coombzy/Project-Car/pull/222) rather than merging it: it prices by the minute, and #226 prices by the hour. The two edits touch the same files.

## What matches your decisions

| Decision | In #226–#232 |
| --- | --- |
| Bookable 24 hours. The price changes by band, the door does not close at night. | Yes. Any whole hour is accepted. |
| Each hour costs that hour's band. | Yes (#226). A Thu 3 p.m.–9 p.m. visit is no longer cheaper than a shorter one that starts later. |
| Whole-hour start and end, 1 hour minimum. | Yes (#227), for a normal booking and for a Bay 6 request. |
| Free cancel at 24 hours or more. Inside 24 hours, keep 50%. | Yes (#231). Exactly 24 hours is free. |
| No-show keeps 100%. | Yes, and only when Sweep runs (#231). |
| Member cannot cancel after the start. | Yes, by the start clock (#231). |
| No refund of unused time once a visit is finished. | Yes (#229). Completing a visit writes no refund. |
| 4 peak hours a week. | Yes (#232), on member bays. Bay 6 approval does not check it. |
| No hold while picking. Re-check at Book. | Already true. A quote holds nothing. Book checks the bay again. The price can still change under that re-check. |
| Any bay = lowest-numbered free bay for the whole span. | Not built. |
| Bay 6 is request-only. | Yes. A direct booking is refused. |
| Labels say Mountain Time. | One bay-closed email says those words. The site, the calendar file, and the fill email still say America/Regina. |
| GST on all transactions. | 5% on a token purchase only, stored inside the token note (#228). |
| No negative balances. | Yes (#229). There is no "allow negative" switch. |
| Damage deposit in dollars. | Not built. The unused dollar field on the member is still unused. |
| One month of allowance rolls over. | Not built. |
| Token packs later. | Not built. A purchase can still be typed in by hand, which is the right manual PayPal step. |

## Ranked findings

Severity is how badly this charges the wrong number of tokens, or blocks a bay, if it ships as it is.

### 1. High — The shop clock has two names, and the safety pin is a separate PR

Typed times (the booking form's plain date box) are read as `America/Edmonton`. Bands, held hours, the peak week, and the monthly grant use `America/Regina`. The website draws the calendar in Regina. The bay-closed email formats the hour in Edmonton and then writes the words "Mountain Time". The fill email writes "America/Regina".

On this machine the zone data is IANA 2026e. Edmonton and Regina are both UTC−6 on 31 Oct 2026, on 1 Nov 2026 at 3 a.m., and on 15 Jan 2027. The offset does not jump. The abbreviation does. Before Sunday 2:00 a.m. Edmonton calls itself MDT. After that it calls itself CST. Regina is called CST all year. A screen that prints the zone's own abbreviation will start saying Central Time on Sunday morning.

Older zone data still does jump. #225's note is right: tzdata 2026.2 still puts Edmonton back to UTC−7 at 1 Nov 2026, 2:00 a.m. The API does not depend on the tzdata package, so a host with that older data stores a typed 4:00 p.m. as 5:00 p.m. on the price grid. The on-the-hour check still passes, because 5:00 is also on the hour. The member asked for 4.

#225 pins `tzdata>=2026.3` and is not part of #226–#232. It does not touch the same files, so it can land beside the stack.

**Where:** `apps/project-car/api/app/shop_time.py` (two zones, and a comment that still says Edmonton is UTC−7 in winter), `apps/project-car/api/app/services/notify.py` (`_mountain_span` uses Edmonton; the fill mail uses Regina), `apps/project-car/web/lib/time.ts` and `lib/calendar.ts` (Regina), `apps/project-car/api/app/routers/member.py` (the booking calendar file).

**Fix:** Pin the zone data (#225) so every machine matches this one. Keep a single UTC−6 clock for typing, pricing, weeks, and months. Print the words "Mountain Time" ourselves. The zone database's own abbreviation becomes CST on Sunday, so it cannot be the label. America/Denver still springs forward and falls back, so that name would move every booking by an hour twice a year.

### 2. High — Merging the stack breaks the booking screen that exists today

#227 refuses any start or end that is not on the hour. The member form is still a free date-time box. Its default is "now plus 72 hours", not rounded, so a fresh visit often opens at something like 4:43 a.m. and sits in the late-night price. Book then returns `not_on_the_hour`, at the top of a long page. #227 says this web follow-up is out of scope. It is the screen the new rule lands on.

The same form's Cancel button is still a one-tap submit, including after check-in, and it never says how many tokens come back. The booking calendar file stores the moment in UTC and comments "Shop local time is America/Regina." A phone in Calgary shows the right moment. The words on the file are the old name.

**Where:** `apps/project-car/web/components/member-booking-form.tsx`, `apps/project-car/web/app/member/schedule/page.tsx`, `apps/project-car/web/components/member-booking-card.tsx`, `apps/project-car/api/app/routers/member.py` (`_booking_ics`).

**Fix:** Ship a small screen change with the API, before the new calendar. Offer whole hours only. Default to the next whole hour inside the day, one hour long. On Cancel, say the rule and the number of tokens coming back before the press counts. Put "Mountain Time" on the schedule, the quote, and the calendar file.

### 3. High — A no-show keeps every token only if someone presses Sweep, and Cancel undoes it

Sweep marks a confirmed visit that reached its end with no check-in as `no_show`, frees the hours, and keeps 100% by writing no refund. Nothing calls Sweep on a timer. Until then the visit stays confirmed, the hours stay taken, and the member's booking limit stays used. Another member cannot have that bay.

The member cannot cancel after the start, so they cannot dodge the fee. The Owner Cancel button can. Owner cancel is allowed on any pending, confirmed, or active visit, and it refunds the whole reserve. A confirmed visit whose end has already passed is still "confirmed" until Sweep. Cancel on it returns every token. The button on today's card is that Cancel.

**Where:** `sweep_no_shows` and `cancel_booking` in `apps/project-car/api/app/services/bookings.py`. The route is `POST /bookings/sweep-no-shows` in `apps/project-car/api/app/routers/bookings.py`. The card is `member-booking-card.tsx`.

**Fix:** When a confirmed visit's end has passed, free the bay and keep the tokens without waiting for a separate button. Owner Cancel on a visit that has started, or that has already ended, must not be a full refund. A swept no-show is already final, which is right.

### 4. High — Tokens still come back after someone is already on the bay

Check-in opens 15 minutes before the start and marks the visit active. Member cancel looks at the start clock, not at check-in. In that 15 minutes the member is on the bay and can still cancel. Inside 24 hours that cancel keeps half and returns half. After the start clock, the member is refused, which matches the decision.

Finishing the visit keeps the full amount and refuses an "unused tokens" number. That part matches. Overdue visits cannot be cancelled, so a late return also keeps the full amount.

Owner cancel of an active visit is the gap. It refunds 100%, and it does not ask for a reason. The adjustment button does ask for a reason. Cancel does not.

**Where:** `CHECK_IN_EARLY_MINUTES`, `check_in_booking`, `_member_cancel_terms`, and `cancel_booking` in `bookings.py`. Owner cancel is `POST /bookings/{id}/cancel` in `routers/bookings.py`, with no reason on the body. [#206](https://github.com/Coombzy/Project-Car/pull/206) tries to stop cancel after check-in and edits the same file. Merge it only as this tighter rule, so it does not bring the full refund back.

**Fix:** Once the visit is checked in, neither a member nor the normal Cancel button refunds it. The charge stays the full reserve through to Finish.

### 5. High — Bay 6 approval skips the 4-hour peak cap

The request path matches the rules. A Bay 6 request does not hold the hour and does not take tokens. It goes through the same hour grid and the same "how far ahead" window as a normal booking, because creating a request calls `preview_reserve`. A 4:30 request is refused. A request past the plan's window is refused. Two people can ask for the same hour; the first approval takes it and the second gets "that hour is already booked."

Approval then creates an ordinary member booking from the saved quote. It checks the balance and the booking limit. It does not check the peak cap, and it does not look at the hour grid again. Saturday is a peak day (finding 6), so an 8-hour Saturday on Bay 6 is allowed and the member is then already over the cap. Closing the bay cancels future bookings and does not touch these requests, so an old request is still there when the bay reopens.

**Where:** `approve_shop_hoist_request` in `apps/project-car/api/app/services/shop_hoist_requests.py`. The cap itself is `check_peak_cap` in `apps/project-car/api/app/services/peak_cap.py`, called only from `create_booking`. Bay close is `_close_over_future_bookings` in `apps/project-car/api/app/routers/hoists.py`.

**Fix:** Run the same peak check when the request is saved and again when it is approved, in the same save as taking the hours. Refuse with `peak_cap` and leave the request unapproved. When a bay closes, drop or pause its open requests with the same notice as the cancelled bookings.

### 6. Medium — "Peak" is the whole of Saturday, including 2 a.m.

The cap counts hours in the 1.5× band `weekend_fri_eve`. The band table, which the stack did not change, is: Friday from 4 p.m., all of Saturday, and Sunday until 9 p.m. Monday through Thursday have no peak hours. A visit that crosses Sunday midnight does not split peak hours across two weeks, because Sunday night after 9 p.m. is the cheap late-night band, and Monday is not peak. The week math (Monday to Sunday on the shop clock) is sound. The tests cover a fifth hour, a mixed Friday, and the Monday reset.

What that means in the shop: four hours on Saturday morning, even at 2 a.m., uses the whole week's peak allowance, and those hours cost 150 tokens, not the late-night 75. Confirm that this is the peak you meant. If peak is Friday evening and weekend daytime only, the band table and the cap are both aimed at the wrong hours.

**Where:** `resolve_band` in `apps/project-car/api/app/services/pricing.py`, `PEAK_BAND_IDS` in `peak_cap.py`, and the band table in `Docs/token-pricing.md`.

**Fix:** Leave the code if all-day Saturday is the rule. If it is not, change the band hours first, then the cap follows, because the cap is "hours in that band" and not a separate list of evenings.

### 7. Medium — Each hour has its own band, then one discount multiplies the whole visit

#226 does the per-hour sum, and it turns off the 7-days-ahead discount and the last-minute surcharge. Those rows stay in the table and price nothing while the switch is off. That matches the earlier recommendation and your per-hour rule.

Tomorrow's deal is still a single multiplier on the whole visit. It applies when any part of the visit overlaps tomorrow 8 a.m.–9 p.m. A 7 p.m.–11 p.m. booking then gets the late-night hours discounted too. With no published offer, the percent is the live one, so it moves when someone else cancels. Book ignores the total on the request (`tokens` is described as ignored) and charges whatever the server computes at that moment. There is no "the price changed" answer.

No hold while picking is the right call. The re-check at Book covers the bay. It also re-prices, quietly.

**Where:** `quote_reserve` in `pricing.py` (fill multiplies the banded total once), `resolve_fill_for_slot` in `apps/project-car/api/app/services/fill.py`, `BookingCreate.tokens` in `schemas.py`.

**Fix:** Apply a published deal only to the hours inside the deal window, and add those hours up. If the total at Book differs from the total on screen, refuse with the new total and write nothing. Until you want the live percent at all, a day with no published deal should cost the plain band price.

### 8. Medium — One month of rollover is decided, and the obvious formula leaks

Nothing in the stack expires tokens. The monthly grant still adds the plan allowance on top of whatever is already there, and only when you press the button. There is no timer.

"One month rolls over" means this, at that same grant, for the Regina month the grant already uses:

- Allowance is the member's plan amount for the new month.
- Spendable is the balance. It already has upcoming visits taken off.
- Expire `max(0, spendable − allowance)` as its own negative line, tagged with the month, once.
- Then add the new allowance, as today.
- Someone who used nothing ends the grant holding two months (the month they kept, plus the new one). That is one month rolling forward.

Holes to close in that same change:

- Do not expire tokens that are already holding a visit. The cap applies to the spendable balance only. A cancel after the grant can put the balance back above two months until the next grant. Leave that refund alone. Say so in the grant note.
- Run the expiry and the grant in one save. A second press in the same month must expire nothing and grant nothing. Tag the expiry line with the month the way the grant line is already tagged.
- Bought tokens are not a separate pile. The balance is one number. If this cap ships, and packs go on sale afterwards, the next grant will wipe a purchase down to one allowance. Change the rule before the first pack is sold: purchases are protected, and the cap applies to allowance only. #228's `token_purchase` line is the marker to sum. Do not wait for a pack catalogue to write that down.
- A member who changes plan mid-month is capped at the new plan's allowance at the next grant. A downgrade expires the difference.
- The grant month is the shop month (the same month boundary as today, UTC−6). It is not the phone's month, and it is not the peak week. The week resets Monday. The allowance resets on the 1st. A Sunday night visit and a Monday morning grant do not share a boundary.

**Where:** `grant_period_allocations` in `apps/project-car/api/app/services/tokens.py`.

**Fix:** Build the formula above as part of the existing grant button. Do not add a second button.

### 9. Medium — GST is 5% on one button, stored as a note

The rounding that is built is the right rounding for a before-tax amount. $12.30 × 5% = $0.615, which half-up turns into $0.62, total $12.92. The test locks that. Subtotal, GST, and total are quantized to the cent before they are added, so they add back exactly. A second credit for the same payment id is refused.

That record lives inside the token row's `meta`, not in dollar columns. A GST return means reading notes. The other way to add tokens, the adjust button, asks for a reason and records no GST. A PayPal payment typed in there has no tax line. Membership fees have no dollar row at all. The damage deposit is not built.

A refundable damage deposit is money you expect to give back. GST belongs on the membership fee and on token packs, at the moment the money is a sale. It belongs on a deposit in the moment the shop keeps it for damage. Charging 5% when the deposit is taken, and again not refunding it when the deposit is returned, over-collects.

**Where:** `record_token_purchase` and `GST_RATE` in `tokens.py`. Adjust is `adjust_member_tokens` in `apps/project-car/api/app/routers/members.py`. `deposit_balance` is on the member model and is still only ever zero.

**Fix:** Give every dollar a real row: before-tax amount, GST, total, payment id, and what it was (fee, pack, deposit taken, deposit returned, deposit kept). Keep the 5% half-up. Point the purchase button at that row, then credit tokens. Leave the adjust button for corrections, not for payments. Build the deposit on those dollar rows, never on the token balance.

### 10. Medium — A finished visit still looks like held tokens in the ledger

Completing a visit sets the booking's reserved amount to 0 and writes no new ledger line. The original "reserve" line stays, and it is the charge. A 100% no-show does the same. A late cancel writes one refund for the half that comes back, and the reserve line stays. The balance is right in all three cases, and a second refund is blocked by the unique index in migration `20261031_0017`.

A history screen that adds up reserve lines with no matching refund will show finished visits and no-shows as still held. The amount is also gone from the booking row, so the receipt has to read the ledger together with the visit status. The design review's history page (one line: "used 375 tokens") needs that join. It cannot read the booking's reserved amount after Finish, because that field is now 0.

The overdue note still says "No money was charged." The tokens were already taken when the visit was booked, and Finish keeps them.

**Where:** `complete_booking` and `_open_late_return` in `bookings.py`. The index is `apps/project-car/api/alembic/versions/20261031_0017_token_purchase_and_ledger_guards.py`.

**Fix:** When history is built, one visit is one line: held, used, or returned, from the visit status plus the ledger lines. Do not sum raw reserve lines and call that "held". Change the overdue note so it does not say the visit was free.

### 11. Low — "Any bay" needs a second try when two people book together

Not built, and the decision is clear: the lowest-numbered member bay that is free for every hour of the visit, never split, never Bay 6. The hour lock (one row per bay per hour) already stops two people taking the same hour. Tests for that lock run on SQLite. CI runs the API suite on SQLite, where the member-row lock does nothing, so two clicks at once for the same person are not proven on Postgres. The lock is in the right place: the member is locked before the balance check and the peak check.

**Where:** the future any-bay branch of `create_booking`. CI is `.github/workflows/shop-os-ci.yml` (`pytest` on SQLite).

**Fix:** Pick the bay in the same save as taking the hours. If Bay 1 loses a race, try Bay 2 before telling the member nothing is free. Return the bay they actually got.

### 12. Low — A visit can sit half-saved, and the peak switch has only one setting

Book on the website creates the visit, then confirms it, as two calls. The create already takes the tokens and the hours, as pending. If the confirm call never arrives, that hold stays until someone cancels it. There is no expiry. A pending visit also counts toward the 4 peak hours.

#232 adds a one-value switch, `PeakOverCapPolicy`, whose only value is "refuse", so a later premium has somewhere to go. The premium is not built. The switch is machinery for a product that is not in this round. A constant of 4 is the whole rule.

**Where:** `apps/project-car/web/app/member/schedule/actions.ts` (create, then confirm), `peak_cap.py`.

**Fix:** Make Book one save that creates and confirms. Drop the one-value switch when the next person touches that file. The cap stays 4.

## Where the two write-ups are now stale

Use your decisions where they disagree with either review.

| Write-up | What it says | What you decided |
| --- | --- | --- |
| Design review, confirm sheet and B16 | "Free to cancel until it starts." | Free until 24 hours before. Inside that, half is kept. After it starts, no cancel. |
| Design review, Finish (D22) | "Left early at…" and refund the unused tokens. | Finishing keeps the full amount. Take that control off the screen. |
| Design review, B12 | No time-zone label, unless the phone is elsewhere. | Say Mountain Time. |
| Design review, B13 | Show 6 a.m.–midnight, tuck the rest. | Every hour is bookable. Tucking night on the phone is fine. Those hours still have to book, at the late-night or peak price. |
| Design review, B4 | Staff may book a member below zero. | No balance goes below zero. #229 already does this. |
| Token review, D1 and the wireframes | Show 8 a.m.–9 p.m., night behind a toggle. | Same as above: bookable all night. #226's note that you wanted no night toggle over-reads the decision. |
| Token review, D20 | Label it "Calgary time." | Mountain Time. |
| Token review, D8 | Also keep packs bought in the last 90 days. | Packs are later. Protect the `token_purchase` lines before the first pack, and do not invent a 90-day rule now. |
| `Docs/token-pricing.md` on the stack | Price the band that contains the start. Winter Edmonton is UTC−7. | Each hour has its own band. The shop clock is permanent UTC−6. |

The design review's other points still stand and are not rebuilt by this stack: the seeded demo cannot book, the pages talk like a notebook, errors speak in the third person and land far from the button, the price sits stale while it reloads, and the phone calendar is five stacked 24-hour grids. Those are the screen rows. They should use the words in the design review's glossary, with the cancel and Finish sentences swapped for the rules above.

## Build rows

In this order. Each row is one pull request a single implementer can finish. The proof is a failing test first, then the fix, same as #226–#232. UI rows also need a phone shot and a desktop shot.

1. **Pin the clock.** Merge #225. Proof already on that branch: a typed 10:00 on 2 Nov 2026 is stored as 16:00 UTC, and Edmonton is still UTC−6 at 1 Nov 2026 3:00 a.m. Do this before the booking stack is deployed anywhere whose zone data is older than 2026c.

2. **One clock, labelled Mountain Time.** Use that UTC−6 clock for typed times, bands, weeks, months, and the website. The schedule header, the quote, the bay-closed email, the fill email, and the booking calendar file say "Mountain Time". They do not say America/Regina, America/Edmonton, MDT, or CST. Proof: a test that formats a 4:00 p.m. shop slot on 15 Jan 2027 as 4:00 p.m. Mountain Time, and a search that fails if member-facing strings contain `America/Regina`.

3. **The current Book button survives the new API.** Whole hours only, default the next whole hour, one hour long, and the bay list does not show "occupied" for right now. Cancel asks first and states the tokens coming back: all of them at 24 hours or more, half inside that, and no cancel once the visit is checked in or the start has passed. Proof: the default window at 1:43 a.m. is 10:00–11:00 the same day; a 4:30 submit never happens; the confirm text contains the token count.

4. **Cancel and no-show match the fee.** A checked-in visit cannot be cancelled for a refund. Owner Cancel uses the same line once the visit has started. A confirmed visit whose end has passed becomes a no-show and frees the bay in the same save, without a separate Sweep press. Sweep can stay as a catch-up button and must still do nothing the second time. Proof: check in 10 minutes early, cancel, get 400 and the same balance; a confirmed visit one minute past its end no longer holds the hour, and the balance is unchanged.

5. **Bay 6 uses the peak cap.** Request and approval both refuse a visit that would pass 4 peak hours in that week, and approval does it in the same save as taking the hours. Closing the bay pauses or cancels open requests and tells the member. Proof: 4 peak hours already booked, a Saturday Bay 6 request is refused; with room in the cap, approval takes the hour and a second approval of the same hour does not.

6. **Confirm Saturday-all-day before changing bands.** No code until you say whether 2 a.m. Saturday is peak. If it is, this row is a sentence in `Docs/token-pricing.md` and nothing else. If it is not, change `resolve_band` and add a test that Saturday 2 a.m. is the late-night 75 and does not count toward the 4.

7. **The price on screen is the price at Book.** A published tomorrow-deal applies only to hours inside 8 a.m.–9 p.m. Hours outside it keep their band price. Book sends the total it showed. A different total returns 409 and writes nothing. A day with no published deal charges the plain band price. Proof: Thu 7 p.m.–11 p.m. with a 25% deal discounts the 7 p.m. and 8 p.m. hours only; a stale total is refused.

8. **Rollover on the grant button.** Use the formula in finding 8. Proof: a member with 2,500 spendable and a 1,500 allowance expires 1,000, then receives 1,500, and a second grant that month changes nothing. A member with 100 spendable and 1,400 held for a future visit expires nothing. A `token_purchase` of 500 is still in the ledger afterwards, and the test names it as not protected yet.

9. **Dollar rows for GST, then the deposit.** One dollar record with before-tax, GST at 5% half-up, total, and payment id. Fees and packs use it, then tokens are credited. A deposit taken and returned writes no GST and no token line. A deposit kept writes GST. Proof: the $12.30 case still yields $0.62; a deposit round-trip leaves the token balance unchanged; keeping $100 writes $5.00 GST.

10. **Any bay.** Lowest-numbered free member bay for the whole span, never Bay 6, same save as the hours, retry the next bay if the first one loses a race. The response names the bay. Proof: Bay 1 busy for one of the hours and Bay 2 free for all of them books Bay 2; two overlapping any-bay requests end with two different bays or one clear refusal when nothing is free.

11. **Book is one save.** Create and confirm together. A failed Book leaves no pending hold. Proof: a refused Book (not enough tokens, or the hour just taken) leaves the balance and the hours unchanged.

12. **The new calendar, after the rows above.** Use the design review's layout (one lane per bay, words plus pattern, day on the phone, week on the desktop, sticky total). Apply the corrections in the stale-write-up table: all hours bookable, night can be tucked, Mountain Time, Bay 6 says "ask first" and sends a request, the sticky bar states the 24-hour cancel rule, Finish does not offer unused time back, and Book is disabled when the balance would go below zero. This is several pulls (lanes, then phone, then desktop, then month). Do not start it by redrawing the cancel copy from the design review.

Rows 1–5 are the ones that make #226–#232 safe to put in front of a person. Rows 6–11 are the rest of the decisions. Row 12 is the calendar, and it should not jump the queue.
