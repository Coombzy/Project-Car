# Doc Hakosuka Todo List

**Owner:** Doc Hakosuka (Hermes on M1 Max)  
**Maintained under:** `Coombzy/Automation/communication/Doc/`  
**Last updated:** 2026-07-25 (Doc: cron provider + VW signups locked)  
**Fleet rule:** No n8n. Orchestration = Hermes + custom adapters + Discord.

---

## P0 — Ops / reliability

- [x] **FIX cron LLM provider pin** — Root cause: `custom:Doc Hak` had **empty api_key** → cron `No LLM provider configured`. Set `api_key: ollama` (Ollama ignores). Jobs pin `provider=custom:Doc Hak` · `model=qwen3.6:35b`. SEALED green 2026-07-25 00:38 MDT exec `b020814b` · job ok · deliver `#tire-shop` restored · schedule active 10:00/16:00 · 16 local API calls · audit `pair-checkin-2026-07-25-0031.md`.
- [x] **VW SIGNUPS locked** — `SIGNUPS_ALLOWED=false` live (Ben account exists). Invitations already false. Token: `DOC_VW_SIGNUPS_LOCKED`.
- [ ] **VW CF cutover** — CF `vault.projectcar.ca` → origin `:8222` → DOMAIN match → drop temp Caddy `:8443` → Ben phone Bitwarden self-host
- [ ] **CF `cloud.projectcar.ca` → NC `:8080`** (Cloudflare Access later)
- [ ] **Refresh `Docs/nextcloud-progress.md`** — moved from `communication/` 2026-07-26; still 2026-07-14 content; include VW lock + cron provider pitfall + Jul 24–25 stacks + CF vault/cloud plan. Stub at old path.
- [x] **Pair check-in cron** — `89e256129ba3` · `0 10,16 * * *` · skill `fleet-pair-checkin` · provider fixed 2026-07-25
- [x] **Nextcloud Docker hub live on Doc** — NC 30.0.17 `:8080` admin `ben`; Desktop seed `/Users/dochak/Desktop/Fleet-Nextcloud`
- [x] **Vaultwarden + Caddy sibling** — origin `:8222`; clients temp `https://localhost:8443` until CF vault hostname
- [x] **projectcar.ca public** — site pages 200 + Apex (watch degraded blips)
- [x] **agent-dream skill (fleet)** — shared `skills/shared/agent-dream/`
- [x] **Daily backup + dream cron exists** — `doc-daily-backup-and-dream` / `0 22 * * *` · same provider pin
- [x] **Backup tiers** — daily / Sunday weekly / 1st monthly
- [x] **Skill role-tailoring / mutual-audit apply** — prior handoffs closed.
- [x] **daily-doc-backup.sh** — `~/.hermes/scripts/`
- [x] **Hermes cron SSOT for 22:00** — do not also load launchd backup (double-zip).

### Pitfall (fleet)
Cron + custom Ollama provider needs a **non-empty** `api_key` in `config.yaml` custom_providers (placeholder `ollama` is fine). Empty key → misleading `No LLM provider configured` even when pin looks correct.

## P1 — Software baseline (when awake)

- [x] **Amphetamine** — installed and running (Ben confirmed 2026-07-12); `/Applications/Amphetamine.app` present; keep active for gateway + long model jobs
- [ ] Install battery app: **coconutBattery** (+ **AlDente** if always-plugged charge limit desired) — not installed
- [ ] Install **Cursor** if missing (Grok build may already be present)
- [x] Homebrew + git + `gh` + jq path (gh auth working as Coombzy)
- [x] Hermes gateway as service + `DISCORD_ALLOW_BOTS=mentions` (+ tire-shop no_thread)
- [x] Ollama for heavy local models (`qwen3.6:35b`, `gemma4:26b`)
- [ ] Tailscale / mesh remote access (Tailscale launch agent present — verify)
- [ ] Monitoring: Stats or iStat Menus

## P2 — Fleet

- [x] Confirm home channel `#doc-garage` + fleet channel `#tire-shop` routing
- [x] Coordinate backup path layout under `backup/Doc/` (protocol aligned)
- [x] **Live skill align** — `fleet-mutual-improvement` v1.4 + handoff/role-tailoring refs rsynced from `skills/shared/` after `08fd950` pull
- [ ] Optional: merge Porsche original skill tarballs if privately shared
- [ ] Ben decision: `approvals.mode: off` on Doc for fleet autonomy (config currently has **no** `approvals` key; launchd bootstrap already hitting host approval gate)

## Done

- [x] Discord presence / check-in path (2026-07-11)
- [x] First git-safe pack + peer audit of Porsche (commit `b798c58`)
- [x] Adopt process skills from Porsche audit list (Doc-side implementations) (2026-07-11)

---

### Notes
- Porsche can help scaffold scripts; **Doc machine must run its own cron** (jobs don’t hop hosts).
- When blocked on Ben (power/login/approvals), surface on `communication/Porsche/Ben-Todo.md`.
- GitHub todos are source of truth for fleet lists (not chat memory alone).
