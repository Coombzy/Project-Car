# Language Unification Plan

**Date:** 2026-11-04  
**Status:** Proposed for Cortana / Lead review  
**Goal:** Align Project Car and pBay (and by extension Liquid Estate) to the same language/stack so shared features, the future core, and agent work stay simple.

## Current state

- **Project Car**: Python (FastAPI) backend, Next.js / TypeScript frontend.
- **pBay**: TypeScript (likely Next.js or similar) backend and frontend.
- Language mismatch makes sharing code, forking, and extracting a core harder than it needs to be.

## Recommendation

**Primary stack for both apps and websites: TypeScript**

- Websites and front-ends already lean TypeScript / React / Next.js. Keep that.
- For the backends / shared core: move toward TypeScript (Node / Fastify / or a lightweight TS service) so the same language covers apps, websites, and the future pBay-as-core.
- Python remains acceptable for one-off scripts or heavy data jobs if needed, but the main application code should converge on TypeScript.

**Why TypeScript over Rust or staying split**
- Vibe coding reduces the Rust learning curve, but the existing codebases and agent tooling are already strongest in TypeScript/Python. TypeScript has the better short-term path for both apps.
- A full Rust rewrite would be cleaner long-term but is larger than necessary right now and would delay eBay testing and Liquid Estate work.
- Staying split forces ongoing translation cost when features move between Project Car and pBay/Liquid Estate.

## Phased approach (minimizes re-work)

1. **Near term (no rewrite)**  
   Keep developing pBay in TypeScript. Project Car stays Python for now. Use the API/custodian model so shared ad data and catalog logic live behind a clear interface. Do not block eBay testing.

2. **Medium term — extract shared core**  
   When pBay has the features that will be shared (ads, pricing, catalog, photos, metrics), extract those into a TypeScript shared package or service. Project Car consumes it via API. Liquid Estate reuses the same package.

3. **Longer term — converge Project Car backend**  
   Gradually move Project Car’s Python backend endpoints that touch shared domains (parts, jobs that involve listings, CRM pieces that overlap) to TypeScript services, or keep thin Python adapters that call the TypeScript core. Full rewrite only if the remaining Python becomes a clear drag.

4. **Websites**  
   Both websites stay TypeScript / React / Next.js. They consume the same catalog and checkout APIs. Branding and filters differ; the data shape does not.

## What does not change immediately

- Proof-first development and red-green cycles.
- Partitioned data folders on the home lab.
- Agent-operated business goals.
- The near-term priority of getting pBay ready for real eBay sales.

## Sequencing notes

- Language work should not block the first real pBay sales tests.
- The shared file structure (see companion doc) can be adopted before the language convergence is finished.
- Cortana / Lead should review this plan before any large migration starts.

## Open questions for review

- Exact shared package layout (monorepo vs separate package).
- How much of Project Car’s domain logic should stay Python long-term vs move.
- Whether a small Rust service is worth it later for performance-critical paths.

---

*Companion document: `Docs/shared-file-structure.md`*
