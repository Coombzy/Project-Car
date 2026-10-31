# Project Car merge order

**Status:** Open stack as of 2026-10-31. Nothing here is merged.
**Tip:** [#262](https://github.com/Coombzy/Project-Car/pull/262) `cursor/extra-hour-pricing-e6d6`
**Do not merge from this file.** It is the order to land the open booking and token pull requests, bottom up.

GitHub numbers are not stack order. [#253](https://github.com/Coombzy/Project-Car/pull/253) sits above [#255](https://github.com/Coombzy/Project-Car/pull/255). [#259](https://github.com/Coombzy/Project-Car/pull/259) sits under [#257](https://github.com/Coombzy/Project-Car/pull/257). [#261](https://github.com/Coombzy/Project-Car/pull/261) sits under [#260](https://github.com/Coombzy/Project-Car/pull/260). Follow the table.

[#225](https://github.com/Coombzy/Project-Car/pull/225) and [#226](https://github.com/Coombzy/Project-Car/pull/226) both base `main`. Land **#225 first**, then **#226 through #232**, then the rest of the chain. That is the order [#236](https://github.com/Coombzy/Project-Car/pull/236) already wrote down, extended through the calendar and v1 work that stacked on #232. Each later row's base is the previous row's head.

[#233](https://github.com/Coombzy/Project-Car/pull/233) and [#236](https://github.com/Coombzy/Project-Car/pull/236) base `main` and are not parents of the booking chain. They are listed after the chain.

Other open pull requests (finance trackers, backlog docs, and older `gb/` rows such as #206, #210, #212, #215, #217) are outside this stack and are not in the table.

## Close, do not merge

| PR | Branch | Why it stays closed |
|----|--------|---------------------|
| [#222](https://github.com/Coombzy/Project-Car/pull/222) | `gb/r99-20261030213706` (base `main`) | Closed 2026-10-31. Prices a booking from the start minute, so a longer booking can cost less. [#226](https://github.com/Coombzy/Project-Car/pull/226) prices each held hour and replaces that approach. Do not reopen it. |

## Booking and token chain (bottom up)

| Order | PR | Base | Purpose | Risk |
|------:|----|------|---------|------|
| 1 | [#225](https://github.com/Coombzy/Project-Car/pull/225) | `main` | Pin tzdata so Edmonton bookings stay on UTC−6. | A wrong or partial pin shifts every later clock. [#242](https://github.com/Coombzy/Project-Car/pull/242) pins the shop clock again and must agree with this one. |
| 2 | [#226](https://github.com/Coombzy/Project-Car/pull/226) | `main` | Price each held hour at its own band and drop lead-time overlays. | Does not contain #225. Merging it first leaves the tzdata pin behind. It also retires the per-minute rule in #222. |
| 3 | [#227](https://github.com/Coombzy/Project-Car/pull/227) | `cursor/per-hour-pricing-b1e6` | Bookings start and end on the hour, with a one-hour minimum. | Fractional holds that older clients still send are refused. |
| 4 | [#228](https://github.com/Coombzy/Project-Car/pull/228) | `cursor/hour-aligned-holds-b1e6` | Tie a `token_purchase` ledger row to the payment id, and guard one ledger write per booking. | Reusing a payment id, including a stand-in id, is rejected as already recorded. |
| 5 | [#229](https://github.com/Coombzy/Project-Car/pull/229) | `cursor/token-purchase-ledger-b1e6` | Require an override reason and actor, keep a zero balance floor, and do not refund unused time. | An owner adjustment with no reason fails, and a booking that would cross zero is refused. |
| 6 | [#230](https://github.com/Coombzy/Project-Car/pull/230) | `cursor/override-audit-and-floor-b1e6` | Closing a bay refunds and notifies its future bookings, or the close is refused. | API only until #254. A close with future bookings moves tokens and sends notices. |
| 7 | [#231](https://github.com/Coombzy/Project-Car/pull/231) | `cursor/close-bay-bookings-b1e6` | Member cancel window, no cancel after start, and a no-show sweep. | A confirmed visit whose end has passed becomes a no-show and keeps the full charge. |
| 8 | [#232](https://github.com/Coombzy/Project-Car/pull/232) | `cursor/no-show-late-cancel-b1e6` | Cap peak-band hours at four per member per week. | A fifth peak hour in the Monday–Sunday shop week is refused. |
| 9 | [#234](https://github.com/Coombzy/Project-Car/pull/234) | `cursor/peak-hour-cap-b1e6` | Member booking calendar: week on desktop, day on a phone. | Layout-only risk is a phone week squeezed into a day, or a desktop day that hides the week. Month stays a heatmap. |
| 10 | [#235](https://github.com/Coombzy/Project-Car/pull/235) | `cursor/member-booking-calendar-0433` | Owner calendar: day list on a phone, week lanes on a desktop. | Owner lanes can drift from the member calendar if the hour payload changes under them. |
| 11 | [#242](https://github.com/Coombzy/Project-Car/pull/242) | `cursor/owner-booking-calendar-0433` | Pin the shop clock to packaged tzdata. | A second pin that disagrees with #225 moves the displayed hour by one. |
| 12 | [#238](https://github.com/Coombzy/Project-Car/pull/238) | `cursor/pin-shop-clock-e6d6` | Label the one shop clock Mountain Time. | The label changes. The zone id stays `America/Regina`. A label can hide a real offset bug. |
| 13 | [#237](https://github.com/Coombzy/Project-Car/pull/237) | `cursor/one-shop-clock-e6d6` | Book whole hours and state the cancel tokens. | Cancel copy on the book screen can drift from the 24-hour rule enforced later. |
| 14 | [#239](https://github.com/Coombzy/Project-Car/pull/239) | `cursor/whole-hour-book-e6d6` | No refund once a visit starts. | Check-in or a started visit keeps the booked tokens. Unused time is not returned. |
| 15 | [#240](https://github.com/Coombzy/Project-Car/pull/240) | `cursor/cancel-and-no-show-e6d6` | Apply the peak cap to Bay 6 and drop requests when it closes. | Closing Bay 6 drops pending requests on that bay. |
| 16 | [#241](https://github.com/Coombzy/Project-Car/pull/241) | `cursor/bay6-peak-cap-e6d6` | Four token bands, and only Peak counts toward the cap. | Evening and off-peak hours no longer count toward the weekly cap. |
| 17 | [#243](https://github.com/Coombzy/Project-Car/pull/243) | `cursor/four-band-hours-e6d6` | Weekly rate chart, open cells, and the peak-hours line read the saved bands, same as the quote and the cap. | If the rate fetch fails, cells fall back to the seeded table until the next load. The quote still uses the saved bands. |
| 18 | [#244](https://github.com/Coombzy/Project-Car/pull/244) | `cursor/rate-chart-e6d6` | Basic is $500 CAD/month plus GST. Premium stays a $750 stand-in. | Premium $750 reads as a real price on signup until Ben confirms it. |
| 19 | [#245](https://github.com/Coombzy/Project-Car/pull/245) | `cursor/basic-plan-price-e6d6` | Book charges the published deal, and only the total it showed. | A stale page whose total no longer matches is refused and writes nothing. |
| 20 | [#246](https://github.com/Coombzy/Project-Car/pull/246) | `cursor/book-shown-price-e6d6` | Grant button rolls one month of allowance. | A second press that month does nothing. Unused allowance above one month expires. |
| 21 | [#247](https://github.com/Coombzy/Project-Car/pull/247) | `cursor/grant-rollover-e6d6` | Dollar rows carry GST for token purchases and deposits. | Kept deposits are taxed at the 5% stand-in. Older dollar rows keep a null tax breakdown. |
| 22 | [#248](https://github.com/Coombzy/Project-Car/pull/248) | `cursor/dollar-gst-row-e6d6` | Any bay is the lowest free member bay for the whole visit. | Two members booking the same hour at once is proved by the opt-in Postgres test in [#264](https://github.com/Coombzy/Project-Car/pull/264). SQLite still cannot show that race. CI does not run it. |
| 23 | [#249](https://github.com/Coombzy/Project-Car/pull/249) | `cursor/any-bay-e6d6` | Purchased tokens survive the monthly grant. | A grant bug here would wipe tokens a member paid for. |
| 24 | [#250](https://github.com/Coombzy/Project-Car/pull/250) | `cursor/purchased-survive-grant-e6d6` | Member Book creates and confirms in one save. | Member book confirms immediately. Owner `POST /bookings` stays pending. Mixing the two paths skips or doubles a confirm. |
| 25 | [#251](https://github.com/Coombzy/Project-Car/pull/251) | `cursor/book-one-save-e6d6` | Member home shows allowance, purchased tokens, and peak hours. | Home figures can drift from the ledger if the cache is rebuilt wrong. |
| 26 | [#252](https://github.com/Coombzy/Project-Car/pull/252) | `cursor/member-balance-view-e6d6` | Sticky bar states the 24-hour cancel rule. | The sentence can drift from the keep percent the API actually charges. |
| 27 | [#254](https://github.com/Coombzy/Project-Car/pull/254) | `cursor/calendar-cancel-rule-e6d6` | Close a bay with a reason and refund future bookings. | The form performs the #230 close. A saved reason refunds real future visits. |
| 28 | [#255](https://github.com/Coombzy/Project-Car/pull/255) | `cursor/bay-close-form-e6d6` | Charge extra hours when a visit is finished. | Each whole hour past the end is charged at that hour's band. If the member cannot pay, the finish is refused and the visit stays open. |
| 29 | [#253](https://github.com/Coombzy/Project-Car/pull/253) | `cursor/finish-extra-hours-e6d6` | Show every hour on the owner week. | Numbered 253 and stacked on #255. A 24-hour grid can hide the 08:00–21:00 booking window. |
| 30 | [#259](https://github.com/Coombzy/Project-Car/pull/259) | `cursor/owner-schedule-hours-e6d6` | Walk one new member through v1 and settle a missed hour on their home. | Member home, dashboard, bookings, and schedule reads settle elapsed no-shows, so a GET can change a balance. |
| 31 | [#257](https://github.com/Coombzy/Project-Car/pull/257) | `cursor/v1-walkthrough-e6d6` | A manual token change sends the reason the ledger requires. | The owner form that omitted a reason no longer saves. |
| 32 | [#256](https://github.com/Coombzy/Project-Car/pull/256) | `cursor/adjust-reason-e6d6` | Record a stand-in GST purchase and set a sign-in password. | The owner can record a purchase and credit tokens with no money movement. |
| 33 | [#258](https://github.com/Coombzy/Project-Car/pull/258) | `cursor/standin-purchase-e6d6` | Keep the Mountain Time hour on booking times. | New booking JSON carries a UTC offset. Older naive rows that were stored as wall time will display shifted if read as UTC. |
| 34 | [#261](https://github.com/Coombzy/Project-Car/pull/261) | `cursor/booking-clock-e6d6` | A new member can sign up and pick Basic without owner conversion. | Default mode creates an active member and grants the month. Waitlist is a fallback the owner turns on. `/signup` is public. |
| 35 | [#260](https://github.com/Coombzy/Project-Car/pull/260) | `cursor/self-serve-signup-e6d6` | Members buy tokens through a stand-in payment adapter. | Any `STANDIN-` id is accepted. No card is charged. A real processor is not registered. |
| 36 | [#262](https://github.com/Coombzy/Project-Car/pull/262) | `cursor/member-purchase-e6d6` | Extra-hour ledger rows fill the pricing column. | The column is the display string. The charge is still the #255 debit. A mismatch would show one price and take another. |

## Beside the chain (base `main`)

| PR | Base | Purpose | Risk |
|----|------|---------|------|
| [#233](https://github.com/Coombzy/Project-Car/pull/233) | `main` | Shop OS colours use the brochure purple and orange. | Independent of booking math. It recolours screens the calendar rows also touch, so landing it changes the look of every later UI branch until they rebase. |
| [#236](https://github.com/Coombzy/Project-Car/pull/236) | `main` | Review of the booking calendar and token plan, including the #225-then-#226–#232 order and the note to close #222. | Docs only. The written order goes stale if a later row retargets its base. |

## Review, 2026-10-31

Read bottom-up from #225 through #263. The tip's shop API, web lint, and layout checks were green. There were no open review threads. #222 is closed. No new feature row was added. Three defects were fixed on the pull request that owned them, and every child above that pull request was restacked.

| PR | What was wrong | What changed |
|----|----------------|--------------|
| [#245](https://github.com/Coombzy/Project-Car/pull/245) | The booking line used the seeded band table. Book charged the server quote. A published fill showed two totals. | The line is built from the quote, including the fill label. The button still charges that same total. |
| [#248](https://github.com/Coombzy/Project-Car/pull/248) | Any-bay skipped a bay whose status was occupied, even when the requested hour was free. The form also sent the preview bay id, so the server never tried the next bay. | Occupied bays stay eligible. Maintenance and locked bays stay out. Any bay submits no hoist id. |
| [#258](https://github.com/Coombzy/Project-Car/pull/258) | SQLite returns a stored UTC instant with no offset. The dashboard strip read that as shop wall time, so a 2 p.m. booking showed at 8 p.m. Seed rows were the other way around: wall time read as UTC. | The strip reads a naive timestamp as UTC. Seed bookings are stored as the same UTC instant the API writes. |

Follow-up on [#243](https://github.com/Coombzy/Project-Car/pull/243): open cells and the "Peak hours this week" line now read the saved bands, same as the chart, the quote, and the cap. The member home peak line was wired when [#251](https://github.com/Coombzy/Project-Car/pull/251) was restacked. A test edits Peak to 1.60 and checks the member chart, the owner chart, the quote, the cap, the open-cell gutter, and the peak line. Children above #243 were restacked. No merge.

Follow-up in [#264](https://github.com/Coombzy/Project-Car/pull/264): two members booked Any bay for the same hour at once on local Postgres. Both had already read Bay 1 as free. With two bays, the bookings landed on Bay 1 and Bay 2. With one bay, the loser got 409 no_bay. No hour was double-booked. The existing savepoint retry held. No product code changed. The test stays opt-in so CI can keep using SQLite. No workflow file was edited.

Left as they are:

- Cancel keep, no-show, piles, GST, the stand-in processor, extra-hour charges, and signup were read against the product rules and not changed.
