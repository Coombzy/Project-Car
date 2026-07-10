# Ben Todo List

**Owner:** Ben (Coombsy)  
**Maintained by:** Porsche under `communication/Porsche/`  
**Last updated:** 2026-07-10

Things that need **Ben’s action, decision, approval, or physical presence**.

---

## P0 — Blocking / security

- [ ] **Decide remote-access path for phone ↔ Porsche** (Hermes Android / Code Mater / VPN / mesh) and pair devices
- [ ] **Security review after compromise concerns** — confirm 2FA recovery paths, password manager state, and which devices are trusted
- [ ] **Grant / re-check macOS permissions** if Porsche hits “operation not permitted” on critical paths (Full Disk Access, Reminders, etc. as needed)

## P1 — This week / high value

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
