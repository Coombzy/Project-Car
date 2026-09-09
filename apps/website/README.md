# apps/website — projectcar.ca public brochure

Static HTML/CSS/assets. Garage owns this tree. Git SSOT: `apps/website/`.

**Live origin:** Cloudflare Worker `projectcar-brochure` Direct Upload of `html/` from `main`. Classic Pages git is skipped pending CF ↔ GitHub auth — plan: [`Docs/brochure-pages-cutover.md`](../../Docs/brochure-pages-cutover.md). Optional local nginx (`docker compose`) still maps to `:8088` if you have the compose network.

## Waitlist

Membership and Contact `POST` JSON to `{PC_SHOP_API_BASE}/waitlist` (`html/shop-config.js`, default `https://api.projectcar.ca`). Fields: `name`, `email`, optional `phone`/`notes`. Interest only — no pricing, no book-now, no shop-is-open claims. e2e PASS.

## Apex / Chat

Deferred. No Apex sidecar, Chat page, or assistant copy. Contact is email and Discord. Backlog: [`Docs/website-improvements.md`](../../Docs/website-improvements.md).

## Hygiene files (in `html/`)

| File | Role |
|------|------|
| `robots.txt` | `text/plain`; `Allow: /`; points at sitemap. No extra Disallow. |
| `sitemap.xml` | Canonical public HTML only (home, about, the-shop, membership, roadmap, contact). No Chat/Apex. |
| `404.html` | Branded not-found page. nginx `error_page 404 /404.html`. Worker should use static `not_found_handling = "404-page"` on next Direct Upload (Zone owns that setting). |
| `favicon.ico` + `assets/favicon.svg` / `favicon-32.png` / `apple-touch-icon.png` | Icon set. Do not use `mcking.jpg` as the favicon. |
| `_redirects` | Chat → Contact 301s, `/` → `/index.html` 302, plus `/shop` → `/the-shop.html` 302. No SPA `/* /index.html 200`. |
| `_headers` | MIME hints for robots/sitemap when the host honors `_headers`. |

## Local verify (from `apps/website`)

```bash
# Static files (no docker)
python3 -m http.server 8088 --directory html
# then:
curl -sSI http://127.0.0.1:8088/robots.txt | head -10
curl -sS http://127.0.0.1:8088/robots.txt
curl -sSI http://127.0.0.1:8088/sitemap.xml | head -10
curl -sS http://127.0.0.1:8088/favicon.ico -o /dev/null -w '%{http_code} %{content_type}\n'
# python http.server returns 404 for unknown paths (generic body).
# nginx serves 404.html with status 404 — see docker compose / nginx.conf.

# Optional nginx (needs image + compose network)
docker compose up -d
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/this-should-404
```

Home must not show “Website progress 10%”. Status line is “Project Underway” only — no invented percentage.
