# AGENTS.md: rules for every coding agent (Project-Car)

This file is for Cursor cloud agents, Grok Build and the local models (Mad Cat / Lightning). Read it before you change anything. `Docs/build-rules.md` is the source of truth; this is the short version plus the commands.

## Hard rules
- Work on your own branch and open a PR to `main`. Never push to `main`, never force-push, never merge (the lead merges after CI is green).
- Never edit `.github/workflows/**`. Never weaken, skip, xfail or delete a test or check, and never raise a visual/pixel/layout-shift threshold to make a check pass.
- No deploys, no DNS/Cloudflare/tunnel changes, no production hosts or credentials, no Stripe. Don't stamp v1 or set any `passes` value in `Docs/features.json` to true.
- Don't invent ids, rates, tokens or vehicle lists. A value only Ben can supply stays a labelled mock or placeholder.
- One row per PR. Stay inside the files the brief names. If you need another file, say why in the PR body.
- Never commit secrets or `.env` files. Never print a token.
- One cloud agent per PR. Rebases, CI fixes and re-proofs go to that same agent.
- No time estimates. Work is sized in rows.

## Commands
- API (`apps/project-car/api`, Python 3.12): `python -m pip install -e ".[dev]"`, then `pytest` (SQLite in-memory; no Postgres needed). One test: `pytest tests/test_x.py::test_name`.
- Web (`apps/project-car/web`, Node 22): `npm ci`, then `npm run lint` (tsc), `npm test` (node --test lib/*.test.ts), `npm run build`. Visual: `npm run visual` (Playwright; `npx playwright install chromium` first).
- CI checks that must be green: `shop-api pytest`, `shop-web lint / typecheck / build`, `shop-web layout-shift / screenshots`.

Run the related tests while you work and the full check once before you open the PR. Don't re-run the whole suite after every edit.

## Proof
- The failing test names the row and is red on main before your fix.
- Visual references live in `apps/project-car/web/visual/screenshots/`. Keep the 0.1 layout-shift cap and 1% pixel cap (`Docs/shop-os-ci.md`).

- Red first: commit the failing test, then the fix that turns it green. Put both shas in the PR body.
- UI changes: before/after screenshots at 390 and 1440 px, as hosted images in the PR body (not committed). Reference screenshots used by a visual test are test files and may be updated for the pages you changed only.

## Pull request
- Title: row heading plus difficulty tag, e.g. `R12: Owner queue shows pending requests [D4 · S3 C4 R3 T2]`. Each score is 1–9: S size, C context, R risk, T test clarity; D is the highest.
- Body: fill `.github/pull_request_template.md` if present, otherwise use: Row, Difficulty, Agent (your cloud-agent id if you have one), Files, Tests run, Proof, and `IF:` lines.
- `IF:` lines state checkable conditions for merging, one per line, e.g. `IF: CI green on head` or `IF: only apps/x/y.ts and its test changed`.

## Where things are
- Rules: `Docs/build-rules.md`, `Docs/shop-os-ci.md`, `Docs/token-pricing.md` (locked rates).
- Queue and backlog: `Docs/queue.md`, `Docs/backlog.md`, `Docs/later.md`.
- Shop OS: `apps/project-car/api` (FastAPI), `apps/project-car/web` (Next.js). Brochure site `apps/website` belongs to another agent; leave it alone unless the brief says otherwise.
- Do not deploy Doc. Do not say the shop is open.
