# Project Car — Docs index

**Canonical:** `Coombzy/Project-Car` → `Docs/`  
**Engineering clone:** `~/src/Project-Car/Docs/`  
**Optional Desktop mirror:** `~/Desktop/Project Car/docs/` (read copy; do not author there)  
**Updated:** 2026-09-07

`Coombzy/Automation/Docs/` is a **historical mirror**. Do not author product specs there.  
`~/Desktop/Project-Car-Docs/` is **retired**.  
Hermes skill `project-car/references/` holds **pointers + agent-only notes**, not a second full copy.

---

## Start here (product lock, 2026-09-06)

| Doc | What |
|-----|------|
| [master-overview-specification.md](master-overview-specification.md) | Vision and map |
| [platform-architecture.md](platform-architecture.md) | Monorepo, stack, bans |
| [project-car-application-specification.md](project-car-application-specification.md) | Shop product v1 (waitlist + Owner hoist booking) |
| [token-pricing.md](token-pricing.md) | Shop OS token pricing v1 (bands + overlay + fill; Owner-editable defaults) |
| [mission-control-architecture.md](mission-control-architecture.md) | Ben-only cockpit over Nextcloud |
| [integration-plan.md](integration-plan.md) | How the pieces connect |
| [high-level-apps-and-business-specification.md](high-level-apps-and-business-specification.md) | Two products + later fitness widget |
| [website-webapp-specification.md](website-webapp-specification.md) | Domain, tunnel, email, public site architecture |

---

## Living ops

| Doc | What |
|-----|------|
| [STATUS.md](STATUS.md) | What’s live, what’s next, locks — start here for 2026-09-06 ~16:16 (`main` `afb37f9`). **`ops.projectcar.ca` LIVE** (staff-on-shift, not Owner-only); `app.` = temporary alias. Calendar #18 + fill #20 + placeholders #21 + cookies #22 + Docs #23/#25 + schedule harden #24 + inventory #26 + Chat #27 + Dashboard #28 are Live. Inventory prefixes locked: B1–B6 / TC / PT (CM later). Chat v1 (human / polling) LIVE on ops/app demo. Build breadth vs Ship-MVP cut stay two gates. Stripe / shop-open / Apex / MC cockpit still need Ben GO. |
| [token-pricing.md](token-pricing.md) | Token pricing lock (bands + overlay; Basic 1000 / Premium 1500; 6 hoists; shop hoist = Owner-only) |
| [website-improvements.md](website-improvements.md) | P0–P4 backlog for projectcar.ca (tick status as work ships) |
| [nextcloud-progress.md](nextcloud-progress.md) | Live hub status on Doc (no secrets) |
| [doc-software-baseline.md](doc-software-baseline.md) | Doc M1 Max apps / settings |
| [home-lab-specification.md](home-lab-specification.md) | Host lock card (stub — do not restore the July skill draft blindly) |
| [api-stay-up.md](api-stay-up.md) | Keep https://api.projectcar.ca up (uvicorn on Doc; Zone owns tunnel). Brochure is Worker `projectcar-brochure`, not Doc `:8088`. |
| [brochure-worker-deploy.md](brochure-worker-deploy.md) | Standing brochure re-deploy: Zone Direct Upload of `apps/website/html` onto Worker `projectcar-brochure`. Classic Pages git skipped. |
| [cors-origins.md](cors-origins.md) | `CORS_ORIGINS` for brochure waitlist from https://projectcar.ca |
| [member-host-cutover.md](member-host-cutover.md) | Member UI → projectcar.ca checklist (plan only; Ben GO before Garage/Zone). Linked from STATUS Next #1. |

---

## Fleet process

| Doc | What |
|-----|------|
| [ai-agents-constitution.md](ai-agents-constitution.md) | Roles and routing |
| [agent-profiles-specification.md](agent-profiles-specification.md) | Hardware + jobs |
| [heartbeat-standards.md](heartbeat-standards.md) | Heartbeat loop; notes go in `MissionControl/Heartbeats/` |
| [security-playbook.md](security-playbook.md) | Incident response |
| [code-mater-android-integration-guide.md](code-mater-android-integration-guide.md) | Phone / Android agent |

---

## Later / do not implement from these

| Doc | Status |
|-----|--------|
| [eBay-Automation-Module-Spec.md](eBay-Automation-Module-Spec.md) | LATER / NOT V1 |
| [estate-sale-app-specification.md](estate-sale-app-specification.md) | LATER / NOT V1 |
| [project-car-integrated-marketplace-specification.md](project-car-integrated-marketplace-specification.md) | LATER / NOT V1 |

---

## Retired stubs (filenames kept so old links resolve)

| Doc | Go here instead |
|-----|-----------------|
| [deployment-guide.md](deployment-guide.md) | Brochure re-deploy: `brochure-worker-deploy.md`. Else platform + MC + nextcloud-progress |
| [phase-0-nextcloud-roadmap.md](phase-0-nextcloud-roadmap.md) | MC Phase A + nextcloud-progress |
| [doc-nextcloud-headscale-setup-guide.md](doc-nextcloud-headscale-setup-guide.md) | Tailscale + MariaDB — not Headscale/Postgres |

---

## Authoring rule

Edit files in this folder on `Coombzy/Project-Car`. After edits: commit + push. Mirror to Desktop **without** `--delete`.
