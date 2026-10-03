# Member cutover sequence

**Status:** Step 1 done on Doc. Steps 2–5 are paper only — not a GO to change Cloudflare. Not shipped.  
**Updated:** 2026-10-03  
**Related:** [member-host-cutover.md](member-host-cutover.md) (full checklist), [member-zone-edge.md](member-zone-edge.md) (Zone traffic map), [doc-unfreeze.md](doc-unfreeze.md), [STATUS.md](STATUS.md) Reality.

This is the order. The long checklists stay in those files. Do not copy them here. Do not execute from this file. A docs merge is not GO.

---

## #88 is on Doc

**#88** (`ae42b87`) is on Doc at checkout `795f301` / `BUILD_ID` `vQRsAOI0JtWYZ_ogRUjgG` (shop code includes **#36** / **#69** / **#88**). Git `main` `6366d62` is finance only (CCJ / SPCX / BTC-ETH logs) after `795f301`. Product brochure tip is still **#82** (`2036a2d`).

Shop-web middleware:

- The guard runs only when the host is `projectcar.ca` or `www.projectcar.ca`. `ops.`, the temporary `app.` alias, and localhost are unchanged.
- Those hosts may render `/member`, `/member/*`, `/_next/*`, and `/favicon.ico` only. `/members` (Owner list) and `/membership` are not Member UI.
- Any other path **307**s to `https://ops.projectcar.ca/login`. This runs before the owner-login redirects, so `/` and `/login` never render on the customer host.

Public `https://projectcar.ca` is still the brochure Worker, so a curl of the public apex does **not** test #88. Public apex `/member` is still **404**.

## Order

1. **Unfreeze + #88 on Doc — done** (2026-10-01 ~19:48 MDT). [doc-unfreeze.md](doc-unfreeze.md). Host-header smoke on Doc `:3000` (2026-10-02), not the public apex:
   - `Host: projectcar.ca` `/login` and `/` → **307** `Location: https://ops.projectcar.ca/login`
   - `Host: projectcar.ca` `/member/login` → **200**
   - `Host: projectcar.ca` `/member` → **307** to member login
   - `Host: ops.projectcar.ca` `/login` → **200**
   - `Host: www.projectcar.ca` `/member/login` → **200**

2. **Zone path-split — paper, Ben GO.** [member-zone-edge.md](member-zone-edge.md). Only `/member` and `/member/*` on apex go to Doc `:3000`. Everything else stays Worker `projectcar-brochure`. Do not point the apex catch-all at shop-web. `www` `/member*` **301**s to `https://projectcar.ca/member*`. Do not 301 all of www. Not done.

3. **`SHOP_MEMBER_COOKIE_PATH_SCOPED` stays OFF** (`Path=/`) until Ben says that www → apex 301 is in. Then `Path=/member`. Cookie stays host-only. No `Domain=.projectcar.ca`. Flag is **OFF**. Not a GO.

4. **Brochure sign-in** ([website-improvements.md](website-improvements.md) P1-6) only after the path-split smoke. Link is `https://projectcar.ca/member/login`. Never www. Never ops or app. Paper only.

5. **Cutting `app.projectcar.ca` is Next #2.** Not required first. [app-alias-cut.md](app-alias-cut.md). Paper only. **Ben GO.**

No Stripe. The shop is not open. No second home PR. No #89 dual-path copy. Do not merge an older docs PR to catch up.

## How to update this file

When a step above actually happens, mark that step the same day and rewrite the four Reality bullets in [STATUS.md](STATUS.md). Do not paste a smoke essay into STATUS. Do not tick a step from a git SHA alone.
