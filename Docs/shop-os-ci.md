# Shop OS CI — GitHub Actions quality gate

**Status:** Living ops (git-only quality gate)  
**Updated:** 2026-10-03  
**Related:** `STATUS.md`, `deployment-guide.md`, `doc-lid-restore.md` (process wake only), `doc-unfreeze.md` (Ben GO pull — **not** this file), `api-stay-up.md`, `shop-web-stay-up.md`, `ai-agents-constitution.md`, `.github/workflows/shop-os-ci.yml`, `apps/project-car/api/README.md`, `apps/project-car/web/README.md`

Plan + runbook for GitHub Actions on **`apps/project-car`**. Merging this file (and the workflow) is a **git-only** quality gate. It is **not** a Doc deploy, **not** a tunnel/live-secret change, **not** a Cloudflare Worker upload, and **not** a license to `git pull` or rebuild shop-web on Doc.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, or Cloudflare ↔ GitHub auth.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Git-only** | CI runs on GitHub-hosted runners against this repo. It never SSHs to Doc, never curls production with write tokens, and never uploads Worker `projectcar-brochure`. |
| **Green CI does not move Doc** | Doc is **unfrozen** at `795f301` / BUILD_ID `vQRsAOI0JtWYZ_ogRUjgG` (was `4cf8924` / `5swmVz-T2CqKEQzTk1ifU`). **#36** / **#69** / **#88** are live on Doc. A green Shop OS CI check is **not** a pull to finance tip `6366d62`. A further checkout move is a new Ben GO (`doc-unfreeze.md`). Lid-restore is process wake only (`doc-lid-restore.md`). |
| **No production credentials** | Workflow uses public install only (`pip` / `npm ci`). No GitHub Actions secrets. No Doc `.env`, no tunnel tokens, no Cloudflare API tokens, no `GOOGLE_OAUTH_*`, no Stripe. |
| **Path-filtered** | Jobs run when a PR (or push to `main`) touches `apps/project-car/**` or `.github/workflows/shop-os-ci.yml`. Docs-only / brochure / finance PRs do **not** pay this tax. |
| **Not a live probe** | Lookout `projectcar-api-health-watch` and public `GET /health` stay ops. This workflow does not replace them. |

---

## What this is

A **quality gate on git** for Shop OS while Doc stay-up stays a separate Lead lane.

| App | Path | Gate |
|-----|------|------|
| **shop-api** | `apps/project-car/api` | `pytest` (SQLite in-memory via `tests/conftest.py` — **no** shop Postgres, **no** Nextcloud MariaDB) |
| **shop-web** | `apps/project-car/web` | TypeScript lint / typecheck (`tsc --noEmit`) + existing `npm test` + `next build` smoke |
| **shop-web visual** | `apps/project-car/web` | Layout shift and screenshot comparison. Job name `shop-web layout-shift / screenshots`. Does not rename the two checks above. |

shop-web has **no ESLint** package. `npm run lint` and `npm run typecheck` both run `tsc --noEmit` (tsconfig already `noEmit`). That is the static gate for app sources. `*.test.ts` is excluded from `tsconfig.json` because those files use Node’s `--experimental-strip-types` runner and `.ts` import specifiers — they are covered by `npm test`, not `tsc`. `npm run build` is compile smoke — pages are `force-dynamic`, so build does **not** need a live Shop API.

Workflow file: `.github/workflows/shop-os-ci.yml`.

---

## What this is not

| Do not | Why |
|--------|-----|
| Deploy / `git pull` / rebuild on Doc | **#36** / **#69** / **#88** are already live on Doc (`795f301` / `vQRsAOI0JtWYZ_ogRUjgG`). This workflow must not pull finance tip `6366d62`. A further pull is `doc-unfreeze.md` — **not** this workflow. |
| Doc lid-restore | Ordered wake stays `doc-lid-restore.md`. CI green does not mean `api.` / `ops.` / `app.` are up. |
| Brochure Worker Direct Upload | Zone / `brochure-worker-deploy.md`. This workflow does not touch `apps/website/`. |
| Classic Pages git / Wrangler from CI | Still skipped (`brochure-pages-cutover.md`). |
| Tunnel / DNS / CORS edge edits | Zone. No Cloudflare tokens in this workflow. |
| Member host / `app.` cut / OAuth | Plan-only docs. Out of scope. |
| Production credentials in GitHub Secrets | Prefer none. Public install only. |

---

## Trigger

```yaml
on:
  pull_request:
    paths:
      - "apps/project-car/**"
      - ".github/workflows/shop-os-ci.yml"
  push:
    branches: [main]
    paths:
      - "apps/project-car/**"
      - ".github/workflows/shop-os-ci.yml"
```

| Event | When |
|-------|------|
| **`pull_request`** | Required. Any PR that touches Shop OS source or this workflow. |
| **`push` to `main`** | Optional confirm after merge (same path filter). |

`workflow_dispatch` is **not** required. Re-run the check from the Actions / PR Checks UI.

Permissions: `contents: read` only. No `pull-requests: write`, no packages, no id-token.

---

## Jobs

Three jobs on `ubuntu-latest`. No shared cache of secrets. No service containers for pytest (`next build` in the lint job does not boot uvicorn). The visual job boots a loopback API on sqlite for screenshots only. It does not deploy.

### shop-api

| Step | Command / action |
|------|------------------|
| Checkout | `actions/checkout` |
| Python | `actions/setup-python` — **3.12** (`requires-python = ">=3.12"`) |
| Install | `python -m pip install -e ".[dev]"` from `apps/project-car/api` |
| Test | `pytest` (`pyproject.toml` `addopts = "-q"`, `testpaths = ["tests"]`) |

Working directory: `apps/project-car/api`. Defaults from `app/config.py` / `.env.example` are enough (Owner/Member demo stubs). Do **not** copy Doc `.env` into CI.

### shop-web

| Step | Command / action |
|------|------------------|
| Checkout | `actions/checkout` |
| Node | `actions/setup-node` — **22** (matches `@types/node`) + npm cache on `package-lock.json` |
| Install | `npm ci` from `apps/project-car/web` |
| Lint / typecheck | `npm run typecheck` (`tsc --noEmit`) |
| Unit tests | `npm test` (existing `lib/*.test.ts`) |
| Build smoke | `npm run build` (`next build`) |

`SHOP_API_URL` may be set to `http://127.0.0.1:8000` for the build step so the compile-time default is explicit. The API process is **not** started.

### shop-web layout-shift / screenshots

Separate job. The check name is `shop-web layout-shift / screenshots`. `shop-api pytest` and `shop-web lint / typecheck / build` keep those names.

| Step | Command / action |
|------|------------------|
| Install | shop-api `pip install -e ".[dev]"` and shop-web `npm ci` |
| Browser | `npx playwright install --with-deps chromium` |
| Build | `bash visual/build-web.sh` (bakes `visual/shop-now.txt` into the client bundle) |
| Check | `npm run visual` (`playwright test`) |

The check covers every shop-web page that exists today, at 390, 768, and 1440 px wide. Reference PNGs live in `apps/project-car/web/visual/screenshots/`. It fails when layout shift goes above 0.1, or when a screenshot differs from its reference by more than 1% of pixels.

Determinism: Liberation Sans and Liberation Mono are vendored and forced through fontconfig. Animations are off. `SHOP_NOW` is `2026-10-06T15:00:00-06:00`. The API is sqlite seeded with `python -m app.seed --reset` on loopback. Quote and ICS download routes are not pages and are not shot.

---

## Roles

| Role | Owns | Does not own |
|------|------|----------------|
| **Lead** | Shop OS sequence. Treats a red Shop OS CI check as a code-quality block on `apps/project-car`. Hands the fix to a Cursor cloud agent / this lane. | Doc `:8000` / shop-web KeepAlive **because CI is red**. CI is not lid-close. |
| **Garage** | Brochure HTML / waitlist e2e after public health is 200 | This workflow. Do not fan Garage from a Shop OS CI fail. |
| **Zone** | Tunnel / DNS / Worker upload | This workflow. No CF token here. |
| **Lookout** | Live probes (`projectcar-api-health-watch` class) | GitHub Actions. A red CI check is not a 530 / 1033. |
| **Chief** | Standing GO for tests / CI. Plan-improve. | uvicorn / shop-web restarts. Doc pull. |
| **Ben** | Doc unfreeze / Member GO / `app.` cut | Do **not** ping for a red pytest or `tsc` fail. Unfreeze after GO is `doc-unfreeze.md`. |

No Ben ping for ordinary CI red. Fix the code, push, re-run.

---

## Failure triage

Read the failed **job** first (`shop-api` vs `shop-web`), then the step.

| Symptom | Likely | Do |
|---------|--------|----|
| `pytest` fail | API regression or fixture/seed assumption | Reproduce locally: `cd apps/project-car/api && pip install -e ".[dev]" && pytest`. Fix tests or app. Do **not** SSH to Doc. |
| `tsc --noEmit` fail | Type error in shop-web | `cd apps/project-car/web && npm ci && npm run typecheck`. |
| `npm test` fail | `lib/*.test.ts` assertion | Same directory, `npm test`. |
| `next build` fail | Compile / Next config / missing types after `tsc` | `npm run build`. Pages are `force-dynamic` — a build fail is **not** “API is down.” |
| `shop-web layout-shift / screenshots` fail | Layout shift above 0.1, or a screenshot past the 1% pixel ratio | Reproduce with the visual commands below. Update a reference PNG only when the page change is intended. |
| `npm ci` / pip install fail | Lockfile / PyPI / npm registry | Re-run once. If persistent, pin/lock in git. Still no secrets. |
| Workflow **skipped** | Path filter | Expected when the PR does not touch `apps/project-car/**` or this workflow file. |
| Public `api.` / `ops.` 530 / 1033 | Doc lid-close | **Not this workflow.** `doc-lid-restore.md`. |

Do **not**:

- Restart uvicorn or shop-web KeepAlive because CI is red
- `git pull` or rebuild on Doc to “make CI match live”
- Curl `https://api.projectcar.ca` with write tokens from Actions
- Upload the brochure Worker from this workflow
- Add GitHub Secrets for Doc / Cloudflare / Google / Stripe to unblock install

---

## How this relates to Doc

CI and Doc are **two clocks**.

| Clock | Tip / pin | What it means |
|-------|-----------|----------------|
| **Git `main`** | `6366d62` (finance only after `795f301`) | Shop OS CI gates PRs that touch `apps/project-car/**`. Green means the **checkout in GitHub Actions** passed pytest / typecheck / build. Product brochure tip is **#82** (`2036a2d`). |
| **Doc working tree** | **UNFROZEN** at **`795f301`** / BUILD_ID **`vQRsAOI0JtWYZ_ogRUjgG`** | **#36** / **#69** / **#88** are live on Doc. Live `ops.` / `app.` / `:3000` are that build. Lid-restore must **not** auto-pull (`doc-lid-restore.md`). A later pull is a new Ben GO (`doc-unfreeze.md`). |

A green Shop OS CI check on finance tip `6366d62` is **expected** and **does not** mean Doc is on that SHA. Green CI is **not** a Doc pull.

---

## Local reproduce (same commands as CI)

```bash
# shop-api
cd apps/project-car/api
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest

# shop-web
cd apps/project-car/web
npm ci
npm run typecheck
npm test
npm run build

# shop-web layout-shift / screenshots
# Needs the shop-api package on PYTHONPATH (`pip install -e ".[dev]"`).
cd apps/project-car/web
npx playwright install --with-deps chromium
bash visual/build-web.sh
npm run visual
```

No Docker, no tunnel, no Doc.

---

## Out of scope

Amending held #70, tip-only finance stamps, Zone Direct Upload, Member host cutover, `app.` alias cut, Google Calendar OAuth implementation, Mission Control cockpit, Classic Pages git, Cloudflare ↔ GitHub auth.
