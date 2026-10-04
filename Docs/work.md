# Work

Living list for Lead and Build. Updated 2026-10-04.

The shop app is the product. The current Doc tunnel and demo cookies are a travel stopgap, not the end. Ben wants a functional app: a member can book a bay, the token ledger is real, and two people cannot take the same hour.

Git only until Ben says otherwise. Do not deploy Doc. Do not cut DNS. Do not add Stripe. Do not say the shop is open. A green check starts the next open row. One item per pass.

`Docs/STATUS.md` is the live stamp. This file is the queue. A row closes only when the proof names it.

## App

| Item | State | Do now | Needs Ben |
| --- | --- | --- | --- |
| Brochure waitlist | Live on projectcar.ca | Leave it. | No. |
| Shop API | On main. Reachable on Doc when the Mac is awake. | Leave the tunnel. | The home machine later. |
| Bookings, hoists, tokens | On main. Shared demo password. | Prove two bookings cannot take the same bay hour. Replace the shared member password with a per-member secret that is not in the README. | No. |
| Member self-serve | On ops and the app alias. Not on projectcar.ca. | Build the member login and booking flow in git for the customer host. Do not upload the Worker. | The path split and the DNS cut. |
| Demo password | In the public README. | Remove `changeme`. Seed refuses it unless the host is loopback. | No. |
| Chat, dashboard, fill | On main. | Leave them working. Do not add a new product. | No. |
| Parts, tools, cameras, payments | Placeholders. | Keep the screens labeled placeholder. Do not add Stripe or a camera feed in this queue. | Stripe, and a shop opening. |
| Staff login | Shared cookie. | Do not add OIDC in this pass. | Ben. |

## Website

| Item | State | Do now | Needs Ben |
| --- | --- | --- | --- |
| Brochure pages | Live on the Worker. | Leave the live origin. | A Pages cutover. |
| Member path on the apex | 404. | Do not flip the Worker. | Ben GO for the path split. |
| app. alias | Still live. | Do not cut DNS. | Ben. |
| Copy that says the shop is open | Must not ship. | A proof that public pages do not say the shop is open. | No. |

## Not this queue

Stripe, the public shop opening, Mission Control, and the finance trackers. Those wait for a GO. Finance commits are not the product tip.
