# Project Car / Mission Control — Stack Exclusions

**Last updated:** 2026-07-10  
**Owner:** Ben (decision) / Porsche (enforcement)

## Hard bans

| Item | Status | Replacement |
|------|--------|-------------|
| **n8n** | Removed 2026-07-10. Do not reintroduce. | Hermes agents, cron/heartbeats, custom webhooks, first-party API adapters, Discord delivery |
| Google as primary personal stack | Eliminate over time | Nextcloud (Files, Calendar, Mail, Contacts, Notes, Deck) |

## Where n8n was purged (reference)

- `~/Documents/mission-control/docker/docker-compose.yml` — no n8n service/volume/env
- Deleted `~/Documents/mission-control/n8n/`
- Dashboard: Hermes Agents panel (not n8n workflows)
- Docs: Desktop Project-Car-Docs, Obsidian Integration Plan, project-car skill references, TASKS/HEARTBEAT

Mentions of n8n that remain should only be **decision/exclusion notes** (“removed / do not reintroduce”), not planned work.

## Orchestration model (allowed)

1. Hermes heartbeats / cron on Porsche  
2. Custom code in Mission Control and integration adapters  
3. Discord (Turbocharger Springs) for human-facing reports and alerts  
4. Nextcloud + Matrix APIs via agents (OCS, WebDAV, Client-Server)  

## Edit rule

When Ben issues a stack ban (“we aren’t using X”), scrub **product usage** everywhere the same turn:

1. Engineering tree (`~/Documents/mission-control/`) + git commit  
2. Skill references under `project-car/references/`  
3. `~/Desktop/Project-Car-Docs/`  
4. Obsidian `~/Documents/Obsidian Vault/Project Car/`  
5. GitHub `Coombzy/Automation/Docs/` when clone/access is available  

Do not leave n8n (or the banned tool) as an open Phase 0/1 checklist item.
