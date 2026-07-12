# Mutual agent audit protocol (Porsche ↔ Doc ↔ McKing)

**Purpose:** Continuous mutual improvement — each agent exports a **git-safe** pack, peer-audits, **adopts+adapts** role-fit ideas, and **recommends** improvements that deepen the peer’s charter. Agents must **not** converge into the same agent.

**Skill (runbook):** `fleet-mutual-improvement` (Hermes skill on each host)  
**Repo:** `Coombzy/Automation` is **public**. Assume every file is world-readable.

---

## 0. Weekly loop (product)

| Cadence | What |
|---------|------|
| **Weekly** | Full mutual-improvement run via skill (export → audit → adopt/adapt → recommend → push → one Discord summary) |
| **On demand** | Same skill when Ben asks or after large skill/config changes |
| **Not daily** | Avoid cost/noise busywork |

Each **machine runs its own** job. Jobs do not hop hosts.

**Cron:** prefer Sunday local morning; keep **paused** while fleet cloud crons are paused unless Ben resumes or pins a local model.

---

## 1. Two backup layers

| Layer | Path | Git? | Contents |
|-------|------|------|----------|
| **Full local** | `backup/<Agent>/{daily,weekly,monthly}/` | **No** (gitignored) | `hermes profile export`, full archives |
| **Git-safe** | `backup/<Agent>/git-safe/` | **Yes** | inventories, skill lists, redacted config, non-secret scripts, audit + adoption + recommendation reports |

Never put on git:

- `.env`, `auth.json`, OAuth tokens, Discord bot tokens
- Full profile `.tar.gz` exports (often embed secrets)
- Raw session DBs / private chat dumps
- Detailed security-incident / 2FA / recovery notes
- Mesh private keys, SSH keys, passwords, hardware serials

---

## 2. Required git-safe files (each agent)

Under `backup/<Agent>/git-safe/`:

| File | Owner |
|------|--------|
| `inventory-latest.json` | Agent (overwrite each export) |
| `inventory-YYYY-MM-DD.json` | Agent (dated snapshot) |
| `AUDIT-PACK.md` | Agent (human-readable + **charter** + will-not-become) |
| `peer-audit-of-<Other>-YYYY-MM-DD.md` | Peer reviewer |
| `adopted-from-audit-YYYY-MM-DD.md` | Owner after applying changes |
| `recommendations-from-<Peer>-YYYY-MM-DD.md` | Peer → subject recommendations |

Inventory should be **Doc-shaped**: hardware (no serials), local_llm, always_on_notes, discord_role_notes, skills, redacted config, scripts, memory hashes/previews only.

---

## 3. Role identity locks (anti-homogenization)

| Agent | Charter | Must not become |
|-------|---------|-----------------|
| **Porsche** | Coordinator / Ben PA / fleet planner / travel host (M4 Pro 24GB) | Doc-style heavy-model primary; skill-parity clone |
| **Doc** | Specialist / heavy compute / local LLM / domain+research (M1 Max 64GB) | Second PA / Ben scheduler |
| **McKing** | Coding + GPU + storage backend | PA clone or pure chat twin |

**Rules**

1. Restate charter every run before adopting anything.
2. **Adapt** ideas to hardware/role — never blind-copy model sizes or persona.
3. Skill count parity is **not** a goal. Unique skills are healthy.
4. Every peer audit needs **Do not copy** + **divergence health** (me-only / peer-only skill counts).
5. Every run publishes **recommendations for the peer** that improve *their* job (two-way improvement).
6. Ben alone rewrites charters or approves security-sensitive exposure.

Full skill: `fleet-mutual-improvement` → `references/role-identity-cards.md`.

---

## 4. Export checklist (each agent, on its own machine)

1. Pull latest Automation repo.
2. Build inventory (public-safe fields only).
3. Write `AUDIT-PACK.md` with charter, strengths, gaps, will-not-become.
4. Commit **only** git-safe + protocol docs. Push (or bundle if no auth).
5. Ping peer in `#tire-shop` with real `@` mention when ready.

---

## 5. Peer audit + adopt + recommend

**Audit gates (all must pass to self-adopt):** role-fit · hardware-fit · non-clone · net value · security.

**Phases (skill):** preflight → self export → peer intake → peer audit → self adoption → recommendations-for-peer → publish + single Discord status → stop (no ack-loop).

**Weakness countermeasures**

| Weakness | Countermeasure |
|----------|----------------|
| Inventory without skill files | Adapted skill_manage create/patch or private skill share — don’t claim install without files |
| Push blocked | Bundle / Ben `gh auth` / peer with write access |
| Homogenization | Charter + do-not-copy + divergence counts |
| Busywork | Require real delta or evidence-based no-op |
| Cloud cost | Weekly only; pause with fleet cloud policy |
| Discord loops | One status post; inline mentions only |

---

## 6. Discord coordination

- 1:1: `#porsche-garage` / `#doc-garage` / `#mcking-garage`
- Fleet: `#tire-shop` (id `1524975356656746547`), mention-only
- `DISCORD_ALLOW_BOTS=mentions` + `bots_require_inline_mention=true`
- Prefer **no auto-thread** on tire-shop (`no_thread_channels`)
- Bot wake-up needs literal `<@bot_id>` in body

---

## 7. Cadence while Ben is away

| When | Who | What |
|------|-----|------|
| Weekly (when cron resumed) | Each online agent | Full skill run |
| ASAP if peer pack missing | Peer | Export + push |
| McKing online later | McKing | Join same skill/protocol |

Cloud cron cost policy still applies until local LLM fleet ready.

---

## 8. Install skill on a host

```bash
# If skill lives on Porsche, copy tree to peer:
# ~/.hermes/skills/autonomous-ai-agents/fleet-mutual-improvement/

# Or re-create from this protocol + skill text in Automation Docs if mirrored.
```

Doc/McKing should install the same skill name so weekly crons load it.

---

**Last updated:** 2026-07-11  
**Status:** Active protocol + `fleet-mutual-improvement` skill; weekly cron created on Porsche **paused** until Ben resumes
