# Shop OS CI — GitHub Actions quality gate

**Status:** Living ops (git-only quality gate)  
**Updated:** 2026-09-08  
**Related:** `STATUS.md`, `deployment-guide.md`, `doc-lid-restore.md`, `api-stay-up.md`, `shop-web-stay-up.md`, `ai-agents-constitution.md`, `.github/workflows/shop-os-ci.yml`, `apps/project-car/api/README.md`, `apps/project-car/web/README.md`

Plan + runbook for GitHub Actions on **`apps/project-car`**. Merging this file (and the workflow) is a **git-only** quality gate. It is **not** a Doc deploy, **not** a tunnel/live-secret change, **not** a Cloudflare Worker upload, and **not** a license to `git pull` or rebuild shop-web on Doc.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, or Cloudflare ↔ GitHub auth.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Git-only** | CI runs on GitHub-hosted runners against this repo. It never SSHs to Doc, never curls production with write tokens, and never uploads Worker `projectcar-brochure`. |
| **Doc checkout stays frozen** | Doc remains at `4cf8924` / BUILD_ID `5swmVz-T2CqKEQzTk1ifU` (Dashboard **#28**) until **Ben GO**. A green Shop OS CI check is **not** that GO. Lid-restore is process wake only (`doc-lid-restore.md`). |
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

shop-web has **no ESLint** package. `npm run lint` and `npm run typecheck` both run `tsc --noEmit` (tsconfig already `noEmit`). That is the static gate for app sources. `*.test.ts` is excluded from `tsconfig.json` because those files use Node’s `--experimental-strip-types` runner and `.ts` import specifiers — they are covered by `npm test`, not `tsc`. `npm run build` is compile smoke — pages are `force-dynamic`, so build does **not** need a live Shop API.

Workflow file: `.github/workflows/shop-os-ci.yml`.

---

## What this is not

| Do not | Why |
|--------|-----|
| Deploy / `git pull` / rebuild on Doc | Checkout frozen at `4cf8924` / `5swmVz`. That would flip **#36** / **#69** live on Doc. |
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

Two parallel jobs on `ubuntu-latest`. No shared cache of secrets. No service containers (pytest uses in-memory SQLite; `next build` does not boot uvicorn).

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

---

## Roles

| Role | Owns | Does not own |
|------|------|----------------|
| **Lead** | Shop OS sequence. Treats a red Shop OS CI check as a code-quality block on `apps/project-car`. Hands the fix to a Cursor cloud agent / this lane. | Doc `:8000` / shop-web KeepAlive **because CI is red**. CI is not lid-close. |
| **Garage** | Brochure HTML / waitlist e2e after public health is 200 | This workflow. Do not fan Garage from a Shop OS CI fail. |
| **Zone** | Tunnel / DNS / Worker upload | This workflow. No CF token here. |
| **Lookout** | Live probes (`projectcar-api-health-watch` class) | GitHub Actions. A red CI check is not a 530 / 1033. |
| **Chief** | Standing GO for tests / CI. Plan-improve. | uvicorn / shop-web restarts. Doc pull. |
| **Ben** | Doc unfreeze / Member GO / `app.` cut | Do **not** ping for a red pytest or `tsc` fail. |

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

## How this relates to Doc freeze

CI and Doc are **two clocks**.

| Clock | Tip / pin | What it means |
|-------|-----------|----------------|
| **Git `main`** | Moves with merges (this repo) | Shop OS CI gates PRs that touch `apps/project-car/**`. Green means the **checkout in GitHub Actions** passed pytest / typecheck / build. |
| **Doc working tree** | Frozen at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**) | Live `ops.` / `app.` / `:3000` stay on that build until **Ben GO**. Lid-restore must **not** auto-pull (`doc-lid-restore.md`). |

A green Shop OS CI check on a later SHA is **expected** and **does not** mean Doc is on that SHA. `#36` (host allowlist) and later shop-web slices stay **on git, not live on Doc** until Lead `git pull` + rebuild **after** Ben GO.

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
```

No Docker, no tunnel, no Doc.

---

## Out of scope

Amending held #70, tip-only finance stamps, Zone Direct Upload, Member host cutover, `app.` alias cut, Google Calendar OAuth implementation, Mission Control cockpit, Classic Pages git, Cloudflare ↔ GitHub auth.
