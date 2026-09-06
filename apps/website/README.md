# apps/website — projectcar.ca public brochure

Static HTML for Cloudflare Pages (cutover planned). Source imported from Doc `~/hermes-tools/project-car-website`; this tree is the git SSOT going forward for the brochure.

## Waitlist

Membership and Contact `POST` JSON to `{PC_SHOP_API_BASE}/waitlist` (`html/shop-config.js`, default `https://api.projectcar.ca`). Fields: `name`, `email`, optional `phone`/`notes`. Interest only — no pricing, no book-now, no shop-is-open claims.

## Apex

Deferred. No Apex sidecar, Chat page, or assistant copy in this Pages-ready tree. Contact is email and Discord. Backlog: [`Docs/website-improvements.md`](../../Docs/website-improvements.md).

## Local (optional)

```bash
docker compose up -d
# http://127.0.0.1:8088/
```
