# v1 launch checklist

**Status:** Checked 2026-11-02. [#225](https://github.com/Coombzy/Project-Car/pull/225) and [#233](https://github.com/Coombzy/Project-Car/pull/233) are merged. [#259](https://github.com/Coombzy/Project-Car/pull/259) is still open. [#222](https://github.com/Coombzy/Project-Car/pull/222) is closed (2026-10-31), not merged. Do not reopen it. Every other pull request in the `merge-order.md` tables is closed and was not merged.
**Related:** `merge-order.md`, `token-pricing.md`

**Merged** means that pull request is on `main`. **Closed** means it was closed and not merged. **Open** means it is still open. **Waiting on Ben** means the real value is not confirmed. The shop is not open. There is no Stripe. Do not merge a closed or already-merged pull request from this file.

## Stand-ins waiting on Ben

| Item | What the stack does now | Status |
|------|-------------------------|--------|
| Payment processor | `PaymentProcessor` is the interface ([#260](https://github.com/Coombzy/Project-Car/pull/260)). The only registered adapter is `stand-in`. It accepts a `STANDIN-` payment id or mints one. It does not call a network. Owner record of a purchase ([#256](https://github.com/Coombzy/Project-Car/pull/256)) also takes a stand-in id and does not go through the adapter. Ops Payments is still the sample page. | Adapter is on closed [#260](https://github.com/Coombzy/Project-Car/pull/260). It is not on `main`. A real processor is **waiting on Ben**. |
| GST rate check | `GST_RATE` is `Decimal("0.05")` (Ben D15). Token purchases and a kept deposit add that rate on the before-tax amount, half-up to cents ([#247](https://github.com/Coombzy/Project-Car/pull/247), [#260](https://github.com/Coombzy/Project-Car/pull/260)). | The 5% rate is on closed [#247](https://github.com/Coombzy/Project-Car/pull/247) and [#260](https://github.com/Coombzy/Project-Car/pull/260). It is not on `main`. Confirmation from Ben's accountant is **waiting on Ben**. |
| Premium price | Basic is **$500 CAD/month** before GST and the owner can edit it. Premium is **$750** before GST on the tier row ([#244](https://github.com/Coombzy/Project-Car/pull/244)). Signup can show both. | Basic **$500** is on closed [#244](https://github.com/Coombzy/Project-Car/pull/244). It is not on `main`. Premium **$750** is a stand-in **waiting on Ben**. |
| Deposit rules | Take and return move the deposit balance and write **no GST** and no tokens. Keep reduces the balance and writes GST at the stand-in rate on the before-tax amount held ([#247](https://github.com/Coombzy/Project-Car/pull/247)). Payment ids are stand-ins. An AI cannot move a deposit on its own. | Ledger behaviour is on closed [#247](https://github.com/Coombzy/Project-Car/pull/247). It is not on `main`. Whether keep should be taxed, and any other keep rule, is **waiting on Ben**. |

## Built on these pull requests

A **Closed** row is not on `main`. Do not merge it from `merge-order.md`.

| v1 item | Where | Status |
|---------|-------|--------|
| Self-serve signup: password, pick Basic, month granted, no owner conversion | [#261](https://github.com/Coombzy/Project-Car/pull/261). Waitlist remains the fallback when the owner sets `signup_mode` to `waitlist`. | **Closed** |
| Member buys tokens and sees GST lines | [#260](https://github.com/Coombzy/Project-Car/pull/260). Owner can still record a purchase by hand ([#256](https://github.com/Coombzy/Project-Car/pull/256)). | **Closed** |
| Whole-hour booking, one-hour minimum | [#227](https://github.com/Coombzy/Project-Car/pull/227), [#237](https://github.com/Coombzy/Project-Car/pull/237) | **Closed** |
| Member Book creates and confirms in one save | [#250](https://github.com/Coombzy/Project-Car/pull/250). Owner create stays pending. | **Closed** |
| Book charges the published deal, and only the total it showed | [#245](https://github.com/Coombzy/Project-Car/pull/245). A day with no published fill deal charges the band price. | **Closed** |
| Four bands. Only Peak counts toward a cap of 4 hours per member per Monday–Sunday week. Lead-time overlays are off. | [#226](https://github.com/Coombzy/Project-Car/pull/226), [#232](https://github.com/Coombzy/Project-Car/pull/232), [#241](https://github.com/Coombzy/Project-Car/pull/241). Bay 6 uses the same cap and drops requests when it closes ([#240](https://github.com/Coombzy/Project-Car/pull/240)). | **Closed** |
| Weekly rate chart on the member booking screen | [#243](https://github.com/Coombzy/Project-Car/pull/243) | **Closed** |
| Cancel 24 hours or more is free. Inside 24 hours keeps 50%. No refund once a visit starts. No-show keeps 100% when it is settled. | [#231](https://github.com/Coombzy/Project-Car/pull/231), [#239](https://github.com/Coombzy/Project-Car/pull/239), [#252](https://github.com/Coombzy/Project-Car/pull/252) are closed. Member home, dashboard, bookings, and schedule settle a missed hour on open [#259](https://github.com/Coombzy/Project-Car/pull/259). | **#259 open**. The cancel pull requests are **closed**. |
| Allowance and purchased piles. Spend allowance first. Purchased tokens survive the grant. Home shows both piles and peak hours this week. | [#246](https://github.com/Coombzy/Project-Car/pull/246), [#249](https://github.com/Coombzy/Project-Car/pull/249), [#251](https://github.com/Coombzy/Project-Car/pull/251) | **Closed** |
| Any bay is the lowest free member bay for the whole visit | [#248](https://github.com/Coombzy/Project-Car/pull/248). A Postgres race between two members is not proven. | **Closed** |
| Owner week shows every hour. Phone is a day list. | [#235](https://github.com/Coombzy/Project-Car/pull/235), [#253](https://github.com/Coombzy/Project-Car/pull/253). Member calendar is week on desktop and day on a phone ([#234](https://github.com/Coombzy/Project-Car/pull/234)). | **Closed** |
| Close a bay with a written reason and refund future bookings | API [#230](https://github.com/Coombzy/Project-Car/pull/230), form [#254](https://github.com/Coombzy/Project-Car/pull/254) | **Closed** |
| Manual token change requires a written reason | API [#229](https://github.com/Coombzy/Project-Car/pull/229), form [#257](https://github.com/Coombzy/Project-Car/pull/257). Balance cannot go below zero. | **Closed** |
| Finish a visit and charge extra whole hours at that hour's band. Ledger pricing column names each hour. | Charge [#255](https://github.com/Coombzy/Project-Car/pull/255), column [#262](https://github.com/Coombzy/Project-Car/pull/262). Peak cap does not block the extra-hour charge. | **Closed** |
| One shop clock, labelled Mountain Time, with a UTC offset on booking JSON | [#225](https://github.com/Coombzy/Project-Car/pull/225) is merged. [#242](https://github.com/Coombzy/Project-Car/pull/242), label [#238](https://github.com/Coombzy/Project-Car/pull/238), and offset [#258](https://github.com/Coombzy/Project-Car/pull/258) are closed and were not merged. The zone id in the API remains `America/Regina` (UTC−6). | **#225 merged**. **#242, #238, and #258 closed**. |
| End-to-end walkthrough of signup, purchase, book, late cancel, no-show, bay close, adjustment, and overtime | [#259](https://github.com/Coombzy/Project-Car/pull/259) is still open. [#261](https://github.com/Coombzy/Project-Car/pull/261), [#260](https://github.com/Coombzy/Project-Car/pull/260), and [#262](https://github.com/Coombzy/Project-Car/pull/262) are closed and were not merged. | **#259 open**. **#261, #260, and #262 closed**. |

## Still to settle before a launch

| Item | Status |
|------|--------|
| [#222](https://github.com/Coombzy/Project-Car/pull/222) is closed (2026-10-31), not merged. Do not reopen it. [#259](https://github.com/Coombzy/Project-Car/pull/259) is the only open pull request in the `merge-order.md` tables. | #222 closed. #259 open. |
| Replace the stand-in payment processor | **Waiting on Ben** |
| Confirm the GST rate | **Waiting on Ben** |
| Confirm the Premium monthly price | **Waiting on Ben** |
| Confirm deposit keep rules (tax on keep, and anything beyond take / return / keep) | **Waiting on Ben** |
| Say whether a live unpublished fill percent should ever price a booking. Today only a published deal does. | **Waiting on Ben** |
| Open the shop and turn on live billing | **Waiting on Ben**. No Stripe in this stack. |
| Month view as bookable lanes | Not in this stack. Month stays the density heatmap. |
| Prove two members cannot take the same any-bay hour on Postgres | Not proven. No workflow or CI change in this stack. |
