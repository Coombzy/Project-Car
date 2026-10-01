# Member cutover sequence

**Status:** Paper only. Not a GO to unfreeze, and not a GO to change Cloudflare. Not shipped.  
**Updated:** 2026-10-01  
**Related:** [member-host-cutover.md](member-host-cutover.md) (full checklist), [member-zone-edge.md](member-zone-edge.md) (Zone traffic map), [doc-unfreeze.md](doc-unfreeze.md), [STATUS.md](STATUS.md) Reality.

This is the order. The long checklists stay in those files. Do not copy them here. Do not execute from this file. A docs merge is not GO.

---

## Already on git — not on Doc

**#88** (`ae42b87`) is on `main` (tip at this pass: `2036a2d`, brochure **#82**). Shop-web middleware:

- The guard runs only when the host is `projectcar.ca` or `www.projectcar.ca`. `ops.`, the temporary `app.` alias, and localhost are unchanged.
- Those hosts may render `/member`, `/member/*`, `/_next/*`, and `/favicon.ico` only. `/members` (Owner list) and `/membership` are not Member UI.
- Any other path **307**s to `https://ops.projectcar.ca/login`. This runs before the owner-login redirects, so `/` and `/login` never render on the customer host.

Doc is still frozen at `4cf8924` / `BUILD_ID` `5swmVz-T2CqKEQzTk1ifU`. Public `https://projectcar.ca` is still the brochure Worker, so a curl of the public apex does **not** test #88.

## Still needed, in this order

1. **Unfreeze** (separate Ben GO). [doc-unfreeze.md](doc-unfreeze.md). Doc must be running #88 **before** any path-split. If Zone sends `/member` at shop-web while Doc is still the frozen build, the customer host would get the ops UI. After unfreeze, smoke **on Doc**, not on the public apex:

   ```bash
   curl -sI -H 'Host: projectcar.ca' http://127.0.0.1:3000/login
   ```

   Expect **307** and `Location: https://ops.projectcar.ca/login`. Same for `/`. `Host: projectcar.ca` on `/member/login` must **not** go there. `ops.` and `app.` stay on the #36 behavior.

2. **Zone path-split.** [member-zone-edge.md](member-zone-edge.md). Only `/member` and `/member/*` on apex go to Doc `:3000`. Everything else stays Worker `projectcar-brochure`. Do not point the apex catch-all at shop-web. `www` `/member*` **301**s to `https://projectcar.ca/member*`. Do not 301 all of www.

3. **`SHOP_MEMBER_COOKIE_PATH_SCOPED` stays OFF** (`Path=/`) until Ben says that www → apex 301 is in. Then `Path=/member`. Cookie stays host-only. No `Domain=.projectcar.ca`.

4. **Brochure sign-in** ([website-improvements.md](website-improvements.md) P1-6) only after the path-split smoke. Link is `https://projectcar.ca/member/login`. Never www. Never ops or app.

5. **Cutting `app.projectcar.ca` is Next #2.** Not required first. [app-alias-cut.md](app-alias-cut.md).

No Stripe. The shop is not open. No second home PR. No #89 dual-path copy. Do not merge an older docs PR to catch up.

## How to update this file

When a step above actually happens, mark that step the same day and rewrite the four Reality bullets in [STATUS.md](STATUS.md). Do not paste a smoke essay into STATUS. Do not tick a step from a git SHA alone.
