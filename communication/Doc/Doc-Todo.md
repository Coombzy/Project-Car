# Doc Hakosuka Todo List

**Owner:** Doc Hakosuka (Hermes on M1 Max)  
**Maintained under:** `Coombzy/Automation/communication/Doc/`  
**Last updated:** 2026-07-25 (Porsche feedback after progress brief)  
**Fleet rule:** No n8n. Orchestration = Hermes + custom adapters + Discord.

---

## P0 — Ops / reliability

- [ ] **FIX cron LLM provider pin (URGENT)** — `doc-porsche-pair-checkin` (`89e256129ba3`) failing repeatedly in `#tire-shop`: `No LLM provider configured`. Pin Hermes custom Ollama provider (not bare `ollama`) + `qwen3.6:35b`. **Pause job until fixed** to stop channel spam. Same pin for daily backup/dream if failing.
- [ ] **VW security cutover** — CF `vault.projectcar.ca` → origin `:8222` → DOMAIN match → drop temp Caddy `:8443` → **`SIGNUPS_ALLOWED=false`** → Ben phone Bitwarden self-host
- [ ] **CF `cloud.projectcar.ca` → NC `:8080`** (Cloudflare Access later)
- [ ] **Refresh `communication/Nextcloud-progress.md`** — still 2026-07-14; live stacks Jul 24–25 (NC + VW + site)
- [x] **Pair check-in cron created (Ben 2026-07-12)** — `89e256129ba3` · `0 10,16 * * *` · skill `fleet-pair-checkin` · deliver `#tire-shop` — **broken until provider pin**
- [x] **Nextcloud Docker hub live on Doc** — NC 30.0.17 `:8080` admin `ben`; Desktop seed `/Users/dochak/Desktop/Fleet-Nextcloud`
- [x] **Vaultwarden + Caddy sibling** — clients `https://localhost:8443`; signups still OPEN (must lock)
- [x] **projectcar.ca public** — site pages 200 + Apex grok-4.5 health ok
- [x] **agent-dream skill (fleet)** — shared `skills/shared/agent-dream/`
- [x] **Daily backup + dream cron exists** — `doc-daily-backup-and-dream` / `0 22 * * *` — verify provider pin
- [x] **Backup tiers** — daily / Sunday weekly / 1st monthly
- [x] **Skill role-tailoring / mutual-audit apply** — prior handoffs closed.
- [x] **daily-doc-backup.sh** — `~/.hermes/scripts/`
- [x] **Hermes cron SSOT for 22:00** — do not also load launchd backup (double-zip).

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
