# apps/website — projectcar.ca public site

Imported from Doc `~/hermes-tools/project-car-website` (live tree). Static HTML + nginx + Apex companion.

## Waitlist

Membership and Contact include a public waitlist form that `POST`s JSON to:

`{PC_SHOP_API_BASE}/waitlist`

Fields: `name`, `email`, optional `phone`, optional `notes`.

Default base URL is `https://api.projectcar.ca` (see `html/shop-config.js`). Override at runtime with `window.PC_SHOP_API_BASE` before the config script, or edit the default for a given deploy. The hostname may not be live until Zone finishes DNS/tunnel.

This is interest capture only — no pricing, no “book now”, no claim the shop is open. Apex on Contact remains chat-only.

## Local

See `docker-compose.yml` / `nginx.conf`. Prefer editing here in git going forward; sync back to the Doc hermes-tools tree when deploying until that cutover is explicit.
