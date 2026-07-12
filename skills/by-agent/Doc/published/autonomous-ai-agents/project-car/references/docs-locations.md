# Project Car — Document Locations Map

Quick map so agents do not search randomly or overclaim what exists.

## Canonical specs (keep in sync)

| Doc family | Skill (`references/`) | Desktop (`~/Desktop/Project-Car-Docs/`) | GitHub `Coombzy/Automation/Docs/` |
|------------|----------------------|----------------------------------------|----------------------------------|
| Master overview | `master-overview.md` | `master-overview-specification.md` | same basename as Desktop when mirrored |
| High-level apps + business | `high-level-apps-and-business-specification.md` | same | same |
| Agent profiles | `agent-profiles-specification.md` | same | same |
| Team constitution | `ai-agents-team-specification.md` | `ai-agents-constitution.md` (name may differ) | Desktop name when mirrored |
| Heartbeats | `autonomous-heartbeat-development-specification.md` | `heartbeat-standards.md` | Desktop name when mirrored |
| Security | `security-incident-response-specification.md` | `security-playbook.md` | Desktop name when mirrored |
| **Integration plan** | `integration-plan.md` | `integration-plan.md` | `integration-plan.md` |
| Grok bridge protocol | `grok-agent-bridge.md` | optional | not required on Docs/ (lives under `communication/`) |

**Rule:** After editing a canonical spec, update skill + Desktop + push `Docs/` on Automation in the same turn.

## Obsidian product notes

`~/Documents/Obsidian Vault/Project Car/`
- `Project Car Overview.md`
- `Project Car - MVP Features.md`
- `Project Car - Architecture Plan.md`
- `Integration Plan.md` — wiki target for `[[Integration Plan]]` (mirrors skill integration-plan)

## Engineering / backlog (not full specs)

`~/Documents/mission-control/`
- `TASKS.md`, `HEARTBEAT_NOTE.md`, compose/scaffolding, `integrations/nextcloud/`, `integrations/matrix/`
- Active focus: Phase 0→1 Matrix + Nextcloud; tool tracking deferred

`~/Documents/ProjectCar/docs/` — machine setup guides (McKing, Doc)

## GitHub Automation (coordination, not full monorepo)

- `Docs/` — fleet-visible Project Car specs (Ben request 2026-07-09)
- `communication/Porsche|Doc|McKing/` — Grok chat channels (capital names)
- **`communication/Porsche/` ops todos (source of truth, 2026-07-10):**
  - `Ben-Todo.md` — Ben actions/decisions
  - `Porsche-Todo.md` — Porsche-owned work
  - `Purchases.md` — ops shopping list
  - `README-Todos.md` — conventions
  - Local clone: `~/Documents/Automation` — procedure in skill `references/ops-todos.md`
- `Project Car Agent Fleet.md`, `Project Car/README.md` — thin; do not treat as full doc set

## Upload recipe for Docs/

```bash
# From a temp clone after Desktop/skill already updated:
gh repo clone Coombzy/Automation /tmp/Automation && cd /tmp/Automation
mkdir -p Docs
cp ~/Desktop/Project-Car-Docs/*.md Docs/
git add Docs/
git -c user.name=Coombzy -c user.email=219446226+Coombzy@users.noreply.github.com \
  commit -m "Docs: sync Project-Car-Docs mirror" && git push origin main
```

Prefer per-file commit messages when changing a single spec (e.g. `Add Docs/integration-plan.md`).
