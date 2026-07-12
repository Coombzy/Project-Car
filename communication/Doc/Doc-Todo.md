# Doc Hakosuka Todo List

**Owner:** Doc Hakosuka (Hermes on M1 Max)  
**Maintained under:** `Coombzy/Automation/communication/Doc/`  
**Last updated:** 2026-07-12  
**Fleet rule:** No n8n. Orchestration = Hermes + custom adapters + Discord.

---

## P0 — Ops / reliability

- [ ] **Skill role-tailoring (2026-07-12)** — follow temporary `communication/Doc/ROLE-SKILL-TAILORING-INSTRUCTIONS.md` → done token `DOC_SKILLS_ROLE_TAILORED` + sha; then file is deleted
- [x] **Mutual-audit apply phase (2026-07-11)** — installed project-car, token_preflight, token_optimizer, hermes-multi-agent-backup, mission-control-development-heartbeat; wrote `backup/Doc/git-safe/adopted-from-audit-2026-07-11.md`
- [x] **daily-doc-backup.sh installed** — `~/.hermes/scripts/daily-doc-backup.sh`
- [ ] **Daily 10pm backup launchd** — script ready; bootstrap still needs host approval (see `adopted-from-audit-2026-07-11.md` plist)
  - Schedule: `0 22 * * *` (10:00 PM local) via `ai.hermes.doc-daily-backup`
  - Local: full/quick Hermes backup into `daily/` with retention (30d daily / weekly / monthly)
  - Git: **sanitized only** (manifests, inventory) — **never** commit `.env` / `auth.json` / tokens (`Coombzy/Automation` is public)
  - Mirror structure used by Porsche under `backup/Doc/{daily,weekly,monthly,git-safe,logs}/`
- [~] **First local backup zip** — Doc reported ~65MB under gitignored `backup/Doc/daily/` (2026-07-11); re-verify path + retention after launchd is loaded

## P1 — Software baseline (when awake)

- [ ] Install Amphetamine (prevent sleep during gateway / model jobs)
- [ ] Install battery app: coconutBattery (+ AlDente if laptop form factor)
- [ ] Install Cursor if missing (Grok build already present)
- [x] Homebrew + git + `gh` + jq path (gh auth working as Coombzy)
- [x] Hermes gateway as service + `DISCORD_ALLOW_BOTS=mentions` (+ tire-shop no_thread)
- [x] Ollama for heavy local models (`qwen3.6:35b`, `gemma4:26b`)
- [ ] Tailscale / mesh remote access (Tailscale launch agent present — verify)
- [ ] Monitoring: Stats or iStat Menus

## P2 — Fleet

- [x] Confirm home channel `#doc-garage` + fleet channel `#tire-shop` routing
- [x] Coordinate backup path layout under `backup/Doc/` (protocol aligned)
- [ ] Optional: merge Porsche original skill tarballs if privately shared
- [ ] Ben decision: `approvals.mode: off` on Doc for fleet autonomy

## Done

- [x] Discord presence / check-in path (2026-07-11)
- [x] First git-safe pack + peer audit of Porsche (commit `b798c58`)
- [x] Adopt process skills from Porsche audit list (Doc-side implementations) (2026-07-11)

---

### Notes
- Porsche can help scaffold scripts; **Doc machine must run its own cron** (jobs don’t hop hosts).
- When blocked on Ben (power/login/approvals), surface on `communication/Porsche/Ben-Todo.md`.
- GitHub todos are source of truth for fleet lists (not chat memory alone).
