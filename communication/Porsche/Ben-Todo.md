# Ben Todo List

**Owner:** Ben (Coombsy)  
**Maintained by:** Porsche under `communication/Porsche/`  
**Last updated:** 2026-07-12 (Amphetamine confirmed on Doc)

Things that need **Ben’s action, decision, approval, or physical presence**.

---

## P0 — Blocking / security

- [ ] **Decide remote-access path for phone ↔ Porsche** (Hermes Android / Code Mater / VPN / mesh) and pair devices
- [ ] **Security review after compromise concerns** — confirm 2FA recovery paths, password manager state, and which devices are trusted
- [ ] **Grant / re-check macOS permissions** if Porsche hits “operation not permitted” on critical paths (Full Disk Access, Reminders, etc. as needed)
- [ ] **Doc `approvals.mode` policy** — Porsche is already full autonomy (`off`). Confirm whether Doc (M1 Max, trusted home host) should also set `approvals.mode: off` so launchd/script bootstrap and long jobs aren’t approval-blocked. Doc will **not** flip this without your OK.

## P1 — This week / high value

- [ ] **Call Capital One and get account activated**
- [x] **Bring Doc Hakosuka (M1 Max) online / reachable** — Discord + `#tire-shop` bot routing working 2026-07-11; mutual-audit packs exchanged
- [x] **On Doc: Amphetamine** — installed and running (Ben confirmed 2026-07-12); keep machine awake for Hermes gateway / long model runs
- [ ] **On Doc (when awake): install battery app** — prefer **coconutBattery** (health) and/or **AlDente** (charge limit if laptop form factor)
- [ ] **On Doc (when awake): install Cursor if missing** — Grok build already present; Cursor for heavy coding sessions
- [ ] **On Doc (when awake): complete Doc software baseline** (see Porsche-Todo Doc stack) — Tailscale verify, monitoring; Homebrew/gh/Ollama/gateway/Amphetamine done
- [ ] **On Doc (when awake): load 10pm backup launchd** — script ready (`daily-doc-backup.sh`); bootstrap was approval-blocked (see Doc adopted-from-audit). One Terminal pass after approvals decision.
- [ ] **Approve Mission Control Phase 0 secrets** — strong `POSTGRES_PASSWORD` / `NEXTCLOUD_ADMIN_PASSWORD` in `mission-control/docker/.env` (don’t commit)
- [ ] **Prove remote access from phone** to Nextcloud / Discord / agent once stack is up
- [ ] **Confirm Matrix for Phase 1 vs Discord-only interim** (open decision)
- [ ] **Confirm fitness backend preference** when ready: wger vs SparkyFitness (can wait until after NC is live)
- [ ] **McKing storage plan** — confirm target capacity / disks / OS for 30–50 TB backend

## P2 — Soon

- [ ] **Git identity** on Porsche if you care about commit author (`git config user.name` / `user.email`)
- [ ] **Cursor setup** (low priority personal tooling)
- [ ] **Google Calendar management** — plan exit path once Nextcloud Calendar is live (low priority while NC is down)

## P3 — Later / product

- [ ] Finalize shop MVP open questions (tool tracking depth, payment processor confirmation)
- [ ] Choose Project Car App stack direction when Phase 2 starts (Capacitor vs Tauri Mobile vs RN)

## Done

- [x] **Remove n8n from stack** — decided 2026-07-10; Porsche scrubbed code + docs
- [x] **Todo system on GitHub** — decided 2026-07-10; lists live under `communication/Porsche/`

---

### Notes for Ben
- Porsche will keep **Porsche-Todo.md** for agent work and **Purchases.md** for buy lists.
- Reply in Discord with “add to my todo: …” or “done: …” and Porsche will update this file + push.
