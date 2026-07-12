---
name: fleet-mutual-improvement
description: "Use when running weekly fleet mutual-audit (Porsche↔Doc↔McKing): export git-safe packs, peer-audit, adopt/adapt ideas without role homogenization, recommend peer improvements, commit adoption notes."
version: 1.0.0
author: Porsche + Ben (Project Car fleet)
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [fleet, multi-agent, audit, mutual-improvement, cron, discord, git-safe]
    related_skills: [hermes-multi-agent-backup, project-car, hermes-agent, token_preflight, xai-model-selection]
---

# Fleet mutual improvement (weekly)

## Overview

Continuous improvement loop across Hermes agents on different machines. Each agent:

1. Re-exports a **public-safe** inventory of strengths
2. Audits peers for **role-fitting** ideas
3. **Adopts + adapts** (never blind clone)
4. Publishes **recommendations for the peer** that deepen *their* role, not yours
5. Reports briefly to Discord (`#tire-shop`)

**Hard goal:** both agents get better **at their jobs**.  
**Hard anti-goal:** agents converging into the same personality, skill soup, or dual-PA / dual-specialist mess.

Canonical repo paths: `Coombzy/Automation` → `backup/MUTUAL-AUDIT-PROTOCOL.md` and `backup/<Agent>/git-safe/`.

## When to Use

- Weekly cron tick for fleet mutual improvement
- Ben asks to “audit Doc / improve each other”
- After large skill/config changes on any fleet host
- Onboarding McKing into the same loop

**Don't use for:** full profile cloning, secret backup to public git, daily mechanical inventory with no adoption, or making skill counts match.

## Role identity (immutable charters)

Load and **restate** your charter every run before adopting anything.

| Agent | Charter (do not dilute) | Home channel | Hardware bias |
|-------|-------------------------|--------------|---------------|
| **Porsche** | Coordinator / Ben PA / fleet planner / travel host | `#porsche-garage` | M4 Pro **24GB** — process, Discord, todos, light local models |
| **Doc Hakosuka** | Specialist / heavy compute / local LLM host / deep research+domain | `#doc-garage` | M1 Max **64GB** — large Ollama, domain modeling, bulk implement |
| **McKing** | Coding lab + GPU + storage backend | `#mcking-garage` | i9 + RTX 5080 + bulk disks — CUDA, receive backups, heavy code |

**Identity lock rules**

1. Never rewrite SOUL/USER to mirror a peer’s persona.
2. Never adopt peer’s **primary job** as yours (Porsche must not become second heavy-model host; Doc must not become second PA).
3. Skill parity is **not** success. Unique skill sets are healthy.
4. Memory: store **adapted** operational facts, not peer’s full identity dump.
5. If a “great idea” only works on peer’s hardware/RAM/GPU, **recommend it to them** — do not force it on yourself.

See `references/role-identity-cards.md` for expanded locks and red flags.

## Public safety (every export)

`Coombzy/Automation` is **public**.

**Never commit:** `.env`, `auth.json`, tokens, full `hermes profile export` tarballs, session DBs, 2FA/compromise detail, hardware serials, private keys.

**Always commit only:** `backup/<Agent>/git-safe/*` inventories, AUDIT-PACKs, peer audits, adoption notes, recommendations, protocol docs.

## Weekly run — ordered phases

### Phase 0 — Preflight (done when: green lights)

- [ ] Confirm **who you are** (Porsche / Doc / McKing) and restate charter in one sentence
- [ ] `git pull` Automation clone (Porsche: `~/Documents/Automation`; Doc may differ)
- [ ] Check git write works (`git push` dry path or `gh auth status`) — if blocked, export locally + Discord handoff (bundle) instead of failing silently
- [ ] Optional: `token_preflight` if using cloud models for a long audit
- [ ] Cloud cost policy: if fleet cloud crons are paused, **do not** invent extra paid cron chains this run

### Phase 1 — Self export (done when: inventory + AUDIT-PACK written)

Produce under `backup/<You>/git-safe/`:

| File | Purpose |
|------|---------|
| `inventory-latest.json` + `inventory-YYYY-MM-DD.json` | Machine-readable |
| `AUDIT-PACK.md` | Human summary + charter + strengths + gaps + **offers for peers** |

Inventory **must** include (Doc-shaped):

- `hardware` (no serials): chip, RAM GB, cores note, model id, public hostname
- `local_llm` / ollama list if any + routing preference string
- `always_on_notes`
- `discord_role_notes`
- skills list with paths + short descriptions
- redacted config structure
- scripts list
- memory **hashes + short previews only** (redact security/PII)

`AUDIT-PACK.md` must include:

1. **Charter** (role lock)
2. **Unique strengths** (what peers should steal *if* it fits them)
3. **Gaps** (what you want from peers)
4. **Will not become** (anti-homogenization statement)

### Phase 2 — Peer intake (done when: peer packs read)

- Pull latest peer `backup/<Peer>/git-safe/`
- If peer pack missing or stale (>14 days): ping peer in `#tire-shop` with `@` + short HANDOFF; still complete **your** export; note blocker in report
- Diff skill paths: only_peer / only_you / shared

### Phase 3 — Peer audit (done when: peer-audit file written)

Write `backup/<Peer>/git-safe/peer-audit-of-<Peer>-YYYY-MM-DD.md` **or** under your git-safe with clear naming — prefer subject’s folder.

Required sections:

```markdown
# Peer audit: <You> → <Peer> (YYYY-MM-DD)

## Role check
- Peer charter restated
- Homogenization risks this week

## Steal / adopt for ME (high value, role-fit)
- Idea → how I will **adapt** it to my charter/hardware

## Recommend for PEER (deepens THEIR role)
- Idea → why it makes them better at *their* job (not more like me)

## Nice-to-have
## Do not copy (role mismatch / RAM / security)
## Security notes
## Divergence health
- Unique skills peer-only / me-only counts
- Verdict: healthy divergence | warning drift | identity risk
```

**Audit filter (must pass each adopt candidate):**

| Gate | Question |
|------|----------|
| Role-fit | Does this improve **my charter** duties? |
| Hardware-fit | Fits **my** RAM/GPU/OS? |
| Non-clone | Am I adapting, not pasting identity? |
| Net value | Beats status quo after maintenance cost? |
| Security | Public-safe? Ben-OK if security-sensitive? |

If any gate fails → **recommend to peer** or reject, don’t adopt.

### Phase 4 — Self adoption (done when: adopted-from-audit written + real changes)

For each approved item:

1. **Adapt** to your host (e.g. Doc 35B policy → Porsche 7B–14B policy)
2. Implement: skill create/patch, memory add (compact), script, config (non-secret), docs
3. Prefer **thin skills + memory facts** over dumping peer SOUL
4. Write `backup/<You>/git-safe/adopted-from-audit-YYYY-MM-DD.md`:
   - Adopted (what/how/adapted)
   - Deferred
   - Rejected + why (role lock)
   - Recommendations sent to peer (summary)

**Completion criterion:** at least one of (a) real skill/config/memory change, (b) explicit “no beneficial delta this week” with evidence from diff. Never empty cheerleading.

### Phase 5 — Peer recommendation packet (done when: recommendations file pushed)

Write `backup/<Peer>/git-safe/recommendations-from-<You>-YYYY-MM-DD.md`:

- Top 3–7 actions that make **peer better at peer’s charter**
- Ordered install list
- Explicit “do not become me” warnings
- Optional: skill payloads you can share (paths) — **offer**, don’t force public commit of large private skill trees unless public-safe

### Phase 6 — Publish + notify (done when: git push + Discord ping)

```bash
cd <Automation clone>
git add backup/
git status   # confirm no .env / tar.gz / secrets
git commit -m "fleet mutual-improvement: <You> YYYY-MM-DD"
git push
```

Discord `#tire-shop` (mention peers):

```text
@Doc @Ben | FLEET_MUTUAL_IMPROVEMENT | <You> | YYYY-MM-DD
- Export: OK
- Adopted: N items (one-liners)
- Rejected for role-lock: …
- Recommendations for <Peer>: link/path
- Divergence: healthy | warning
- Commit: <sha>
```

Use real `<@bot_id>` mentions for bot wake-up. Prefer parent `#tire-shop` (no dual auto-thread mess).

### Phase 7 — Stop (anti-loop)

- **One** status post. Do not ACK-chain peers unless they `@` you with new work.
- Do not schedule recursive crons from this job.
- Do not pull peer’s entire skill tree “for parity.”

## Adaptation patterns (steal → reshape)

| Peer idea | Bad clone | Good adaptation |
|-----------|-----------|-----------------|
| Doc 35B Ollama | Install 35B on 24GB Porsche | Routing policy + smaller model class |
| Porsche PA todos | Doc becomes second scheduler | Doc keeps specialist; uses GitHub todos only for **Doc-Todo** |
| Heartbeat coding loop | Both run identical overnight cloud burns | Doc: local bulk ticks; Porsche: supervise/architecture |
| Security hardening | Same blind checklist | Travel host vs always-on lab threat models differ |
| Token optimizer | Ignore on local-only host | Doc uses before Grok; local-only skips |

## Weakness countermeasures (built-in)

| Known weakness | Rule |
|----------------|------|
| Inventory without skill payload | Prefer adopt via skill_manage; if peer skill missing, write **adapted** skill from public teachings OR request private skill tar — never claim “installed” without files |
| Git push blocked | Bundle / Ben auth / peer with write access; never drop work on the floor |
| Homogenization | Charter restated every run; Do-not-copy section mandatory; divergence counts mandatory |
| Busywork audits | Require adoption report with real delta or evidence-based no-op |
| Cloud cost | Weekly only; use local model if configured; respect paused-cloud policy |
| Secret leak | Pre-commit mental scan; refuse full profile export to git |
| Role envy | Recommend upward to the right agent instead of self-installing wrong role tools |
| Ack loops on Discord | Single report; `bots_require_inline_mention` discipline |

## Cron design

- **Schedule:** weekly (e.g. Sunday 10:00 local) — not daily
- **Skills to load:** `fleet-mutual-improvement` (+ optional `token_preflight`, `hermes-multi-agent-backup`)
- **Prompt:** use `references/weekly-cron-prompt.md` verbatim (self-contained; cron has no chat memory)
- **Deliver:** `#tire-shop` or `discord:1524975356656746547`
- **While cloud crons paused:** keep job **paused** until Ben resumes or pins local model
- **Each machine runs its own job** — Porsche does not run Doc’s export

## McKing join path

When McKing comes online: same skill, charter = coding+storage, first run is export-only + read Porsche/Doc packs; no identity clone from either.

## Common Pitfalls

1. **Cloning persona** — adopting peer tone/memory wholesale  
2. **Skill count chasing** — installing everything peer has  
3. **Ignoring RAM** — 35B on 24GB  
4. **Public secrets** — profile tar / .env in Automation  
5. **Skipping recommendations-for-peer** — loop becomes one-way theft  
6. **Dual-@ auto-thread races** — post status in parent tire-shop with no_thread policy  
7. **Declaring success without files** — no commit, no adoption note  
8. **Running daily** — cost + noise; weekly is the product

## Verification Checklist

- [ ] Charter restated; identity lock respected  
- [ ] git-safe export updated (inventory + AUDIT-PACK)  
- [ ] Peer audit includes Do-not-copy + divergence health  
- [ ] Adoption note lists adapted/rejected items  
- [ ] Recommendations-for-peer file written  
- [ ] No secrets in `git status`  
- [ ] Pushed to origin (or explicit transport blocker documented)  
- [ ] Single Discord summary with real mentions  
- [ ] No recursive cron created  

## Skill catalog (Automation/skills)

Fleet skill visibility without dumping entire trees every week:

```
skills/
  shared/                      # fleet-wide full skills
  by-agent/<Agent>/
    MANIFEST.json              # all skills: name, path, description, hash
    README.md
    published/                 # full SKILL.md trees opted for sharing
```

**Weekly export:** always refresh your `MANIFEST.json`. Promote full skill bodies to `published/` only when useful for peers (or when recommending install). Default stays **catalog-only** to avoid public-repo bloat and secret risk.

## Related paths

- Protocol: `Automation/backup/MUTUAL-AUDIT-PROTOCOL.md`  
- Packs: `Automation/backup/{Porsche,Doc,McKing}/git-safe/`  
- Skill catalogs: `Automation/skills/by-agent/{Porsche,Doc,McKing}/`  
- Templates: `references/templates.md`  
- Role cards: `references/role-identity-cards.md`  
- Cron prompt: `references/weekly-cron-prompt.md`
