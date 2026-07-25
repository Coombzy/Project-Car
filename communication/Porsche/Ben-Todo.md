# Ben Todo List

**Owner:** Ben (Coombsy)  
**Maintained by:** Porsche under `communication/Porsche/`  
**Last updated:** 2026-07-25 (Doc↔Porsche progress sync)

Things that need **Ben’s action, decision, approval, or physical presence**.

---

## P0 — Blocking / security

- [ ] **Decide remote-access path for phone ↔ Porsche** (Hermes Android / Code Mater / VPN / mesh) and pair devices
- [ ] **Security review after compromise concerns** — confirm 2FA recovery paths, password manager state, and which devices are trusted
- [ ] **Grant / re-check macOS permissions** if Porsche hits “operation not permitted” on critical paths (Full Disk Access, Reminders, etc. as needed)
- [ ] **Doc `approvals.mode` policy** — Porsche is already full autonomy (`off`). Confirm whether Doc should also set `approvals.mode: off`.
- [ ] **Cloudflare public hostnames (Ben / CF dashboard)** — create `vault.projectcar.ca` → Doc `:8222` and `cloud.projectcar.ca` → Doc `:8080` when ready (Access later for cloud). Doc implements origin; Ben owns DNS/Access if only he has CF admin.
- [ ] **On Porsche: install Tailscale** — not present 2026-07-25; needed to reach Doc hub as client
- [ ] **On Porsche: install Bitwarden app** — point at self-host URL after vault CF cutover (or TS URL interim)
- [ ] **On Porsche: install Nextcloud Desktop** — client only; connect to Doc hub
- [ ] **Lock Vaultwarden signups** after first accounts — `SIGNUPS_ALLOWED=false` (Doc can do; confirm with Ben)

## P1 — This week / high value

- [ ] **Call Capital One and get account activated**
- [x] **Bring Doc Hakosuka (M1 Max) online / reachable** — Discord + stacks live Jul 2026
- [x] **On Doc: Amphetamine** — installed and running (Ben confirmed 2026-07-12)
- [x] **projectcar.ca public** — site + Apex chat live (verified 200 / health ok 2026-07-25)
- [ ] **On Doc: battery app** — coconutBattery and/or AlDente
- [ ] **On Doc: Cursor if missing**
- [ ] **On Doc: fix Hermes cron provider** — pair-checkin/dream failing “No LLM provider configured”; pin Ollama custom provider (Doc)
- [ ] **Prove remote access from phone** to Nextcloud / Discord / Bitwarden once vault+cloud hostnames up
- [ ] **Confirm Matrix for Phase 1 vs Discord-only interim** (open decision)
- [ ] **Confirm fitness backend preference** when ready: wger vs SparkyFitness
- [ ] **McKing storage plan** — target capacity / disks / OS for 30–50 TB backend

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
