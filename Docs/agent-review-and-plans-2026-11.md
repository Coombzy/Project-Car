# Agent Review and Plans — 2026-11-04

Living document capturing assessments, structural recommendations, integration gaps, and forward plans discussed for Project Car, pBay, and Liquid Estate. Intended for Cortana and subsequent agents to review point-by-point.

This file preserves detail from the multi-agent review conducted while Cortana was token-exhausted. It does not replace STATUS.md, queue.md, or AGENTS.md. It is an input to those.

## 1. Current Remaining Work (from living docs)

### Project-Car
- STATUS (2026-10-06 stamp): Not shipped — Member UI on projectcar.ca, Zone path-split, `app.` cut, Stripe, shop opening, Mission Control (all Ben GO). Brochure Worker live; Shop OS live on Doc (ops. + temporary app.).
- queue.md Now: Harden job claim and job done (detailed tests, advisory locks, seed behavior). Repo is second; wait for pBay rows on main.
- later.md: Member path, app. DNS, Stripe, shop opening, staff OIDC, etc. (Ben-gated).
- features.json: All entries `passes: false` by rule even when behavior is on main.

### pBay
- STATUS: v1 not closed. No features in features.json marked passing. Local v0 running. No production host.
- queue.md: No open row. Coding lead writes next from backlog.
- Next real exit: sandbox token + category/policy/location ids + 3 photos + two real listing ids both ended.
- later.md: Those credentials/ids, fee table, production host, payout, real listing ids.

**Suggestion**: Refresh STATUS stamps, carve an `active-backlog.md`, and never leave the queue empty.

## 2. Agent Scripts and Efficiency

Scripts live in `scripts/` in both repos (shared core: `next-row.sh`, `related-tests.py`, `prove.sh`, `pr-ready.sh`, `check-if.py`, etc.). Cortana bot was token-exhausted at the time of review; box-only scripts were not in git.

### Key efficiency points
- `related-tests.py` already maps changed files → relevant tests only (big win). Default development path should use it; full suite only at final green.
- Giant pbay proof files (`v0-proof.ts` ~181 KB, `ui-proof.ts` ~132 KB) dominate token and time cost. Modularize + cache.
- Add `agent-context.sh` so agents stop re-fetching STATUS/queue and hitting rate limits.
- Empty queue should auto-surface the next concrete backlog row.
- Expected gain from making `related-tests` the default: 5–15× fewer test-seconds/tokens on intermediate turns.

**Suggestion**: Make related-tests the documented default loop; modularize proofs; commit box scripts when tokens return.

Local models (Mad Cat / Lightning) are listed in AGENTS.md as readers of the rules. No dedicated launchers were found in either repo. Hardware notes exist (Ollama on Doc, GPU on McKing). Shared `scripts/` are what they are expected to use.

## 3. Repo Structure Consistency

The two repos do not share the same top-level layout. This adds friction for agents and humans.

**Suggestion**: Align on a common shape (`AGENTS.md`, `Docs/` with STATUS/queue/later/active-backlog/features.json, `scripts/` as shared or synced, `apps/` repo-specific). Factor near-identical scripts into one source of truth.

## 4. Code Analysis Summary

### Project-Car
- `apps/project-car/api`: FastAPI + SQLAlchemy 2 + Alembic. Clean router/service split (`main.py` is small and clear). Dedicated Postgres.
- Strong domain model for bookings, tokens, hoists, chat, jobs, tool crib, parts requests, etc.
- `app/models.py` (~50 kB): ~30 models + 20+ enums. Well-structured internally but a god file.
- Auth is explicit v1 stubs (Owner cookie/bearer, Member cookie). No OIDC yet (as designed).
- Seed + tests exist; shop is deliberately not open; no live Stripe.

### pBay
- `apps/api`: Node 22 + TypeScript + `node:sqlite` (WAL, foreign keys). Single-process HTTP server in `main.ts` (~25 kB).
- Data layer is one large `store.ts` (~96 kB) that owns schema creation, migrations-via-ALTER, and most business logic.
- UI: large `App.tsx` (~50 kB), `screen.ts` (~43 kB).
- Schema evolution: `CREATE TABLE IF NOT EXISTS` + repeated try/catch `ALTER TABLE`.
- Proof-driven: large `scripts/*-proof.ts` files.

Both follow the proof-first, no-production-without-Ben rules. Project-Car is more conventionally layered; pBay is more “everything in a few big files” for speed of agent iteration.

### Structural issues
1. Repo layout mismatch.
2. God files (`models.py`, `store.ts`, `main.ts`, UI files).
3. Schema evolution style differs (Alembic vs ad-hoc ALTER).
4. No shared contracts or extractable core between the two.
5. Duplicated agent-loop scripts.

## 5. Future Vision: Liquid Estate and Dual-Channel

### Clarified intent
- Liquid Estate will be two things:
  1. A re-branded version of pBay focused on estate sales rather than auto parts.
  2. A website that takes all the ads created for eBay and puts them on a website where people can buy them without eBay.
- The same direct non-eBay purchase function will also be created on the Project Car website, since it would be easy to adapt.

### Fit with current code and docs
- Re-branded pBay for estate matches existing direction (estate template, vertical tags, roadmap Phase 6 “still one pBay core”).
- `liquid-estate-web` is currently an empty placeholder (initial commit 2026-10-31, one-line README only).
- Direct website / non-eBay channel is new relative to checked-in specs (previously parked as “Non-eBay channels”).
- Project-Car integrated-marketplace spec is marked LATER / NOT V1 but already contemplated a customer portal.

### Structural implications
- Same core (items, drafts, photos, condition, pricing, audit) can serve both eBay and direct sites.
- Critical: single inventory truth. A sale on any channel must atomically make other channels out-of-stock (same pattern as current CA/US sibling-withdraw).
- Direct site needs its own checkout/payment (new surface).
- Listing snapshot should be shared so channels cannot diverge.
- Estate vs parts differences should be vertical flags or config, not forks.
- Agent policies must cover both channels.

### Recommended layout
- Shared selling core (today’s pBay, later extracted or kept as single source of truth).
- Thin branded front-ends: `liquid-estate-web` and projectcar.ca direct-buy section. Both call the same public catalog + reservation + checkout API.
- Do not grow either front-end into its own inventory or order system.

## 6. Layout Assessments

### Project Car
**Not the best possible layout** given the stated goals (agent-operated business, job/quote CRM, dual-channel direct sales, convergence with pBay).

Good:
- Clear API/web separation.
- Thin routers, services layer, Alembic, explicit state machines and append-only events.
- Proof-first workflow and hard lines.

Not optimal:
- `models.py` god file.
- Repo-level inconsistency with pBay; no shared contracts.
- No explicit agent principal or policy surface yet (Owner/Member first).
- Breadth placeholders mixed with proven flows.
- Soft boundary between public site and shop OS; no clean public catalog API.

### pBay
**Not the best layout** for the multi-channel, multi-brand, shared-core future, though effective for current agent-driven local v0.

Good:
- Explicit agent API with actors, idempotency, audit, event log.
- Hard refusals in the right places.
- Estate template foothold.
- One-item / two-offers model.

Not optimal:
- `store.ts` (~96 kB) god file (schema + rules + queries).
- Long imperative route table in `main.ts`.
- Large UI files.
- No clean public/read boundary for catalog + reservation.
- Manual schema evolution.
- Channel and vertical logic inline.
- Heavy repo-local proofs.

### Liquid Estate
No real layout yet (empty repo). Intended layout should be a thin front-end over the shared core, not a third independent stack.

## 7. pBay Layout Changes — Top Priority

These changes should be top priority. They enable the estate re-brand and dual direct-buy sites without a later extraction, make every subsequent row cheaper for agents, are incremental and proofable, and do not require stopping the eBay personal-items test.

### Size
Small-to-medium if done incrementally; medium if done as a single extraction. Roughly the same size as (or slightly smaller than) Phase 1–2 of the Project Car job/quote CRM.

| Change | Relative size |
|--------|---------------|
| Split `store.ts` into schema + domain services + channel helpers | Medium |
| Turn long `main.ts` route table into explicit route modules | Small |
| Add thin public catalog + quantity-reservation API | Small-to-medium |
| Move estate vs parts and eBay vs direct differences behind flags/interfaces | Small |
| Modularize large `*-proof.ts` files | Small-to-medium |
| Align repo-level scripts / add `agent-context.sh` | Small |

### Practical priority order
1. Modularize the large proof files + add `agent-context.sh` (immediate efficiency, near-zero risk).
2. Extract route modules and a thin public catalog read API (unblocks both front-ends).
3. Split `store.ts` into schema / domain services / channel helpers while keeping external behavior identical.
4. Add the quantity-reservation primitive as soon as the first direct-channel consumer is ready.

The personal-items eBay credential path can proceed in parallel on the current code.

## 8. eBay Integration Issues

Direction is correct (REST Sell Inventory + Account; Trading API avoided for new writes). Concrete gaps remain.

### Documented blockers
- Sandbox user token (`EBAY_SANDBOX_USER_TOKEN`) via Vaultwarden naming; path does not do OAuth consent itself.
- Per-site category, payment, fulfillment, return-policy, and merchant-location ids empty (not invented).
- Three real `https://` image URLs required; current path does not call Media API.
- Launch-readiness check (one inventory item, two offers, sale sets quantity to 0 then withdraws sibling) not yet written or confirmed on real sandbox.
- Production host refused until Ben names a site.

### Design and completeness gaps
- Condition mapping exists but depends on the table being correct.
- No Taxonomy/Metadata calls yet → missing required specifics will reject publishes.
- Policies and location must already exist on the seller account.
- Multi-site quantity-0 + sibling withdraw is mocked but not confirmed on real sandbox.
- Fee table is a placeholder.
- Error mapping from eBay is still thin.
- Photo hosting / object-store choice still open.
- All of the above currently live inside the large `store.ts` / `main.ts` path.

No fundamental mismatch with eBay APIs. Issues are missing seller-account artifacts, unexercised real-sandbox confirmation, and monolithic placement of the integration logic. Layout split makes them cheaper to close.

## 9. Pricing Calculation Issues

Pricing is intentionally a placeholder and has gaps relative to real eBay fees or dual-channel use.

### What exists
- Fee table (`fee-table.json`): explicit `"placeholder"`. EBAY_CA 1000 bps + 500 minor shipping allowance; EBAY_US 1200 bps + 800 minor. “Not an eBay schedule.”
- FeeSketch: `profit_minor` = price − marketplace_fee − shipping_allowance − other_fee. Does not move money. Assumptions recorded.
- Volume pricing: simple tiered percent discounts (buy 2/3/4+), 80 % cap, truncated. “Stand-in.”
- Suggested price from pasted Product Research; separate CAD/USD with no stored FX; optional `cost_minor` (NULL if omitted).

### Issues
1. Rates are not real eBay fees (ignore category, insertion vs final value, promoted, processing, etc.).
2. Profit ignores cost basis (`cost_minor` not subtracted).
3. No currency conversion between CA and US.
4. Shipping allowance is a flat minor amount (not calculated).
5. Volume tiers disconnected from actual eBay multi-quantity rules.
6. No path yet from sketch to actual post-sale fees (Finances API reserved).
7. No channel dimension — same sketch cannot cleanly serve eBay and direct sites.

Arithmetic that exists is correct; the model is deliberately incomplete. Usable as a rough guide for personal-items test if treated as such. Needs real rates (or Finances reconciliation), cost-basis inclusion, and channel awareness for agent-operated or dual-channel pricing. Small, well-bounded additions once pricing is easy to reach after the layout split.

## 10. Project Car Job / Quote / Shop CRM Plan

Goal: Add ability to quote and perform full repair and modification jobs (labour + parts) for members/customers, and manage related selling of labour, parts, and subscriptions, as a first-class domain inside Project Car. Structured so proven slices can later be opened to agent operation.

### What already exists (reuse)
Members, bookings/bay hours, job events (simple claim/done), parts requests, token/pricing rules, chat, todos, dashboard, staff-action audit style, explicit state machines + append-only events.

### Phase 1 — Core job + quote data model and API
- Models: `Job` (or `WorkOrder`), `Quote`, `QuoteLine` (labour or parts), `JobEvent`.
- Job: member_id, optional vehicle/project note, status, promised date, linked booking_id (nullable).
- Quote: job_id, status (draft/sent/approved/rejected/expired), totals, customer_approved_at.
- Line: kind (labour/parts), description, hours or qty, rate or unit price, extended.
- Status pipeline (minimal): `draft` → `quoted` → `approved` → `in_progress` → `ready` → `closed` (plus `cancelled`).
- API (Owner first): create job, add/edit lines, send quote, record approval, advance status. Member can view own.
- All writes produce audit/event rows. Same error shape.
- Alembic migration. Seed one demo job.
- Proof: cannot advance to `in_progress` without approval; line totals match; member sees only own; second approval idempotent.
- Out of scope: Stripe, live purchasing, agent actor, polished UI.

### Phase 2 — Links to existing shop objects
- Optional link Job ↔ Booking.
- Optional link parts lines to parts-request or inventory concepts (no live purchasing).
- Labour lines can reference existing token/pricing rules as rate source.
- Dashboard / member view shows open jobs.

### Phase 3 — Customer approval and basic desk UI
- Member can view quote and post approval/rejection.
- Owner desk: job list, quote builder, status pipeline.
- Clear “why this job cannot advance” messages.

### Phase 4 — Agent-ready surface (after 1–3 proven)
- Agent principal (or scoped token) with least privilege.
- Explicit policies, e.g. agent may create draft and send quote; may not mark approved or closed; may advance approved → in_progress only when approval exists and bay free.
- Escalation event on blocked action.
- All agent writes audited.

### Phase 5 — Billing hand-off (when Stripe GO exists)
- Approved lines become billable record.
- Subscription or parts-only sales can reuse the same pattern.

### Cross-cutting
- Proof-first, one row per PR, no production deploy, shop remains “not open” until Ben GO.
- Prefer new models in a split file if acceptable (avoid second god file).
- First suggested queue row: “Add Job, Quote, and QuoteLine models + Alembic migration + basic Owner create/read routes + failing proof that status cannot reach in_progress without customer approval.”

This is a well-bounded addition, comparable in size to the existing booking + token ledger work. Not a large new system.

## 11. Agent-Operated Business Direction

Intention is to move both apps to full agent operation (self-managing businesses) once proven.

### Current state
- Both have explicit state, append-only events, and hard safety refusals.
- pBay is closer: primary interface is already the agent API.
- Project Car is sequenced “prove first, then commit to agent operation” because it is more complicated (money, physical bays, members). This is correct and compatible with the end state.
- Missing layer on both: machine-readable decision policies (“agent may do X when Y, else escalate”).

### pBay
Structured the right way for an agent-run selling desk once live eBay path, order/tracking/mail, and policies land.

### Project Car
Right direction (evented, auditable). Needs agent principal + policy layer + gated integrations (payments, opening, staff) before it is equally agent-runnable. Job/quote domain gives a concrete business object for agents to manage.

No fundamental redesign required. Incremental policy surface on top of existing structures.

## 12. Additional Improvement Areas

- Observability: lightweight append-only run log; structured request logs.
- Human onboarding: single `Docs/START-HERE.md`.
- Security hygiene: consistent request-size/field-length limits; image URL host allow-list later.
- Data safety: documented backup step before schema changes (especially pBay SQLite).
- CI tightness: make critical pBay proofs required checks; record timing in PR bodies.
- UI/operator experience: clearer “why cannot publish” messages; map common eBay rejections to plain language.
- Fleet hand-offs: short RACI or `Docs/fleet-handoffs.md`.
- Dependency hygiene: periodic audit cadence.

These are secondary to the pBay layout priority and the job/CRM plan.

## 13. Consolidated Priorities for Cortana

1. **pBay layout changes** (modularize proofs, public catalog API, split `store.ts`, quantity reservation) — top priority.
2. Personal-items eBay sandbox → live path (credentials, ids, launch-readiness check) — parallel, does not wait on layout.
3. Project Car job/quote CRM Phase 1 (data model + basic API + proof).
4. Shared contracts / thin public API so Liquid Estate and projectcar.ca direct-buy remain thin front-ends.
5. Agent policy surface on proven slices (both apps).
6. Repo structure alignment and box scripts committed when tokens allow.
7. Pricing: real rates or Finances path, cost basis, channel awareness (after layout makes it easy).

All preserve existing hard lines: no production without Ben GO, no secrets in git, one writer per files, proof-first, do not stamp v1 green.

## 14. Completeness Percentages (judgment, 2026-10-06 / review date)

### pBay
- Current scoped v0 platform: ~70–75 %
- Production-ready / first real sale: ~25–30 %
- Full long-term (live + estate + direct channel): ~15–20 %

### Project Car
- Current Shop OS demo: ~65–70 %
- Public member-facing + operationally open: ~35–40 %
- Full long-term vision: ~20–25 %

Official features.json understates progress due to the passes rule.

---

*Document created 2026-11-04 from multi-agent review. Cortana (or Lead) to accept, reorder, or amend. Subsequent rows should reference this file where relevant.*
