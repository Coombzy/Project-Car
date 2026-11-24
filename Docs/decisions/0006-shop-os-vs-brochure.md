# ADR 0006: Shop OS vs brochure site

**Status:** accepted

**Decision:** Shop OS is `apps/project-car` (FastAPI + Next.js). The public brochure and waitlist live in `apps/website` and are maintained separately. Agents working on Shop OS leave the brochure alone unless the brief names it.

**Why:** Clear ownership boundaries reduce cross-app churn and accidental deploy scope.

**Source:** `AGENTS.md` (Shop OS paths, brochure note); repo layout under `apps/`.

**Consequences:** No deploys from agent rows. Do not state the shop is open. CORS may allow brochure origins for waitlist APIs; still one product boundary.