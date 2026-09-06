# Project Car — Website & Email Plan
**Date:** 2026-07-24  
**Status:** Live tunnel + landing page; email not yet configured  
**Domain:** projectcar.ca (Cloudflare Registrar + Tunnel)  
**Site path:** `/Users/dochak/hermes-tools/project-car-website`  
**Public:** https://projectcar.ca (Coming soon)

---

## 1. Current state

| Piece | Status |
|--------|--------|
| Domain registered (Cloudflare) | Done |
| Tunnel healthy → `localhost:8088` | Done |
| Static “Project Car / Coming soon” | Done (Nginx Docker) |
| DNS A (proxied) | Live |
| MX / Email Routing | **Not set** |
| Real product pages / app | Not started |
| Agent mailboxes @projectcar.ca | **Not set** |

**Separation of concerns**
- **projectcar.ca** = Project Car public brand + future app  
- **Mission Control** = internal hub (Nextcloud, Vaultwarden, agents) — not the public site  
- Agents (Doc, Porsche, McKing) get **identity addresses** on the domain; they do not need full Google Workspace seats on day one

---

## 2. Website plan (phased)

### Phase 0 — Now (done / polish)
- [x] Tunnel + static landing  
- [ ] Optional: `www` → apex redirect in Cloudflare  
- [ ] Optional: better OG image / favicon  
- [ ] Flush DNS on Doc if browser stale  
- [ ] Park only public marketing on apex; keep `cloud.` / `vault.` off public or behind Access later  

### Phase 1 — Brochure (1–2 weeks of light work)
**Goal:** Credible public face; no full app yet.

| Page | Purpose |
|------|---------|
| `/` | Hero, one-liner, CTA (contact / waitlist) |
| `/about` | What Project Car is (shop OS / fleet / marketplace direction — match existing specs) |
| `/contact` | Form or `hello@projectcar.ca` |
| `/status` or link | Optional uptime note |

**Stack stay simple:** static HTML/CSS (current) **or** small Astro/Next static export later. Stay on Nginx Docker; same tunnel origin `localhost:8088`.

**CTA options**
- Email `hello@projectcar.ca`  
- Waitlist form → Formspree / Basin / Cloudflare Worker → email  
- Link to Discord only if intentional public community  

### Phase 2 — App shell (after Porsche reset + MC stable)
**Goal:** Authenticated or public product surface under subdomain.

| Host | Role |
|------|------|
| `projectcar.ca` / `www` | Marketing |
| `app.projectcar.ca` | Product UI (ProjectCar-App) |
| `api.projectcar.ca` | API (when ready) |
| `status.projectcar.ca` | Optional |

Tunnel public hostnames → separate Docker services.  
**Do not** put Vaultwarden/Nextcloud on naked marketing domain without Cloudflare Access.

### Phase 3 — Marketplace / modules
Align with existing specs:
- `project-car-integrated-marketplace-specification.md`
- `high-level-apps-and-business-specification.md`
- Estate sale / eBay modules as spokes consuming Mission Control data

### Design direction (short)
- Dark industrial / shop floor (current landing is a good base)  
- Mobile-first  
- Fast, few deps  
- Accessibility: contrast, focus states  
- Brand: “Built for the work. Tuned for the road.” (iterate freely)

### Content SSOT
| Asset | Location |
|--------|----------|
| Live static files | `project-car-website/html/` |
| This plan | `Project Car/docs/website-and-email-plan.md` (copy) + Desktop mirror |
| Product specs | existing `Desktop/Project Car/docs/*` |

---

## 3. Email system — goals

Addresses we want early:

| Address | Who / what | Priority |
|---------|------------|----------|
| `ben@projectcar.ca` | You (human) | P0 |
| `hello@projectcar.ca` | Public contact | P0 |
| `doc@projectcar.ca` | Doc Hakosuka (agent / ops) | P0 |
| `porsche@projectcar.ca` | Porsche agent | P0 |
| `mcking@projectcar.ca` | Lightning McKing agent | P0 |
| `noreply@projectcar.ca` | Transactional send-only later | P1 |
| `support@` / `billing@` | When customers exist | P2 |
| Catch-all `*@projectcar.ca` | Optional → Ben (careful with spam) | P1 |

**Agents don’t need a full Outlook seat.** They need:
1. **Inbound** identity (people/systems can mail them)  
2. **Outbound** ability later (Hermes SMTP / notifications)  
3. Credentials in **Vaultwarden**, not Discord/git  

---

## 4. Recommended architecture (practical)

### Tier A — Start this week (free / fast): Cloudflare Email Routing

**Receive-only forwarding** on projectcar.ca → real inboxes you already use.

```
Internet → MX (Cloudflare Email Routing)
        → rule: doc@projectcar.ca     → your Gmail (or label)
        → rule: porsche@projectcar.ca → same or other
        → rule: mcking@projectcar.ca  → same
        → rule: ben@ / hello@         → Ben primary
```

**Pros:** Free, native to Cloudflare, DNS auto, works in minutes, no new mail server on Doc/McKing.  
**Cons:** Cloudflare does **not** host a mailbox UI; **sending as** @projectcar.ca needs an extra step (below).

**Destination options**
- Single Gmail + filters/labels (`doc@`, `porsche@`, …) — simplest  
- Or separate Gmail / Fastmail aliases if you want hard separation  

### Tier B — Send as @projectcar.ca (add soon after Routing)

Pick one:

| Option | Cost | Notes |
|--------|------|--------|
| **Gmail “Send mail as”** + SMTP (Resend, Brevo, Mailgun, SES, SMTP2GO) | Free–low | Best DIY with Routing |
| **Google Workspace** Business Starter | ~$7–8 CAD/user/mo | Real mailboxes; heavier |
| **Microsoft 365** | similar | If you prefer M365 |
| **Zoho Mail** free/cheap | low | Limited free tier |
| **Fastmail** / Proton with custom domain | mid | Privacy-oriented |

**Recommendation for Project Car now:**  
1. **Cloudflare Email Routing** for all inbound @projectcar.ca  
2. One primary destination (your Gmail) + labels  
3. **Resend** or **Brevo** SMTP + Gmail “Send mail as” for `ben@` and `hello@`  
4. Agent addresses: receive via Routing; outbound later via Hermes SMTP using `noreply@` or agent-specific senders when needed  

### Tier C — Later (McKing)
- Optional self-hosted (Stalwart / Mailcow / Maddy) **only** if you want full control  
- Requires clean rDNS, PTR, warm IP, abuse handling — **not** week-one  
- Prefer keeping mail at Cloudflare + SaaS SMTP until app volume demands more  

---

## 5. Cloudflare Email Routing — setup steps (you in dashboard)

### 5.1 Enable
1. Dash → **projectcar.ca** → **Email** → **Email Routing**  
2. **Get started** / Enable  
3. Add **destination address** = your real inbox (Gmail)  
4. Confirm the verification email Cloudflare sends  

### 5.2 DNS
Cloudflare usually adds automatically:
- MX records → Cloudflare Email Routing  
- TXT SPF for routing  

Do **not** add conflicting MX from Google until you intentionally move to Workspace.

### 5.3 Custom addresses (create these)

| Custom address | Action | Destination |
|----------------|--------|-------------|
| `ben@projectcar.ca` | Forward | your Gmail |
| `hello@projectcar.ca` | Forward | your Gmail |
| `doc@projectcar.ca` | Forward | your Gmail (label `agent/doc`) |
| `porsche@projectcar.ca` | Forward | your Gmail (label `agent/porsche`) |
| `mcking@projectcar.ca` | Forward | your Gmail (label `agent/mcking`) |

Optional: **Catch-all** → Ben (expect spam; enable only if you want).

### 5.4 Gmail labels / filters
For each `To: doc@projectcar.ca` → apply label `Project Car/Doc`, skip inbox or not as you prefer.

### 5.5 Send as (after destination works)
1. Sign up **Resend** (or Brevo) → domain `projectcar.ca`  
2. Add DNS TXT (SPF/DKIM) they give you in Cloudflare DNS  
3. Gmail → Settings → Accounts → **Send mail as** → `ben@projectcar.ca` via their SMTP  
4. Repeat for `hello@` if needed  

Store SMTP secrets in **Vaultwarden** only.

---

## 6. Agent identity model (Doc / Porsche / McKing)

| Agent | Email | Use |
|-------|--------|-----|
| **Doc** | `doc@projectcar.ca` | Heavy compute ops notices, reports people reply to |
| **Porsche** | `porsche@projectcar.ca` | Coordinator / travel / scheduling threads |
| **McKing** | `mcking@projectcar.ca` | Lab / GPU / storage / backup alerts |
| **Ben** | `ben@projectcar.ca` | Human authority |

**Hermes later**
- `himalaya` / SMTP skill for outbound from Doc when SMTP exists  
- Inbound: still via Gmail API or forwarding to a processed mailbox — phase 2  
- Do **not** run open SMTP relay on home IP  

**Discord remains** bot-to-bot realtime; email is for humans + external systems + audit-friendly threads.

---

## 7. Security / deliverability checklist

- [ ] SPF (Cloudflare Routing + send provider)  
- [ ] DKIM (send provider)  
- [ ] DMARC `p=none` → `quarantine` when stable (`_dmarc.projectcar.ca`)  
- [ ] No open catch-all if spam hurts  
- [ ] VW store: domain registrar, CF, Resend/Brevo, Gmail app passwords  
- [ ] 2FA on Cloudflare and Google  
- [ ] Never commit SMTP keys  
- [ ] Separate `noreply@` for automated mail when app sends volume  

---

## 8. Decision summary (recommended defaults)

| Decision | Choice |
|----------|--------|
| Public site host | Docker `project-car-website` + tunnel (current) |
| Marketing vs app | Apex marketing; `app.` later |
| Inbound @projectcar.ca | **Cloudflare Email Routing** |
| Human inbox | Your existing Gmail (labels) |
| Outbound brand mail | Resend/Brevo + Gmail Send-as (near term) |
| Full Workspace | Only if you want native multi-mailbox UX soon |
| Self-hosted mail on McKing | Defer |
| Agent addresses | doc@, porsche@, mcking@, ben@, hello@ |

---

## 9. Execution order (next actions)

### Today / this weekend
1. [ ] Enable **Email Routing** on projectcar.ca  
2. [ ] Verify destination Gmail  
3. [ ] Create `ben@`, `hello@`, `doc@`, `porsche@`, `mcking@`  
4. [ ] Send test messages to each; confirm receipt + labels  
5. [ ] Save CF + mail notes in Vaultwarden  

### Next
6. [ ] Add Resend/Brevo domain + DKIM  
7. [ ] Gmail Send-as `ben@projectcar.ca`  
8. [ ] DMARC p=none  
9. [ ] Website Phase 1 pages (about/contact)  
10. [ ] After Porsche reset: mail apps use aliases only; no new personal domains  

### When app exists
11. [ ] `app.projectcar.ca` tunnel route  
12. [ ] Transactional `noreply@`  
13. [ ] Hermes SMTP for agent digests (optional)  

---

## 10. What I need from you to proceed hands-on

1. **Destination inbox** for forwards (e.g. primary Gmail address) — you can set in CF without telling me the address if preferred  
2. Confirm agent list: `doc@` / `porsche@` / `mcking@` / `ben@` / `hello@` OK?  
3. Send path preference: **Routing + Resend/Gmail** (recommended) vs **Google Workspace** now  
4. Optional: Cloudflare **API token** (Zone DNS + Email Routing edit) if you want me to configure DNS/rules via API later  

I cannot finish Email Routing clicks without your CF dashboard (or API token). I **can** draft exact DNS records, Worker form, and website Phase 1 pages as soon as you confirm 2–3.

---

## 11. Quick reference — live infra

```
projectcar.ca  → Cloudflare proxy → Tunnel → host cloudflared
                                         → localhost:8088
                                         → Docker project-car-website (Nginx)

Email (target):
projectcar.ca MX → Cloudflare Email Routing → Gmail (labels per agent)
```
