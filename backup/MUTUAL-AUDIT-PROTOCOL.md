# Mutual agent audit protocol (Porsche ↔ Doc ↔ McKing)

**Purpose:** Each agent exports a **git-safe** inventory of what makes it useful; peers review and adopt improvements without sharing secrets.

**Repo:** `Coombzy/Automation` is **public**. Assume every file is world-readable.

---

## 1. Two backup layers

| Layer | Path | Git? | Contents |
|-------|------|------|----------|
| **Full local** | `backup/<Agent>/{daily,weekly,monthly}/` | **No** (gitignored) | `hermes profile export`, full archives |
| **Git-safe** | `backup/<Agent>/git-safe/` | **Yes** | inventories, skill lists, redacted config, non-secret scripts, audit reports |

Never put on git:

- `.env`, `auth.json`, OAuth tokens, Discord bot tokens
- Full profile `.tar.gz` exports (often embed secrets)
- Raw session DBs / private chat dumps
- Detailed security-incident / 2FA / recovery notes
- Mesh private keys, SSH keys, passwords

---

## 2. Required git-safe files (each agent)

Under `backup/<Agent>/git-safe/`:

| File | Owner |
|------|--------|
| `inventory-latest.json` | Agent (overwrite each export) |
| `inventory-YYYY-MM-DD.json` | Agent (dated snapshot) |
| `AUDIT-PACK.md` | Agent (human-readable summary) |
| `peer-audit-of-<Other>-YYYY-MM-DD.md` | Peer reviewer |
| `adopted-from-audit-YYYY-MM-DD.md` | Owner after applying peer suggestions |

---

## 3. Export checklist (each agent, on its own machine)

1. Pull latest `Automation` repo.
2. Build inventory:
   - skill paths + short descriptions
   - redacted `config.yaml` structure (keys only / secrets scrubbed)
   - non-secret scripts under `~/.hermes/scripts/`
   - cron *schedules and purposes* (no embedded credentials)
   - role, home Discord channel, hardware notes
   - **sanitized** memory previews or hashes only (not full personal/security text)
3. Write `AUDIT-PACK.md` with:
   - unique strengths
   - gaps / “what I want from peers”
4. Commit **only** `git-safe/` + protocol docs. Push.
5. Ping peer in `#tire-shop` (or garage threads): “git-safe export ready for audit.”

---

## 4. Peer audit checklist

When reviewing the other agent’s pack, look for:

1. **Skills** you lack that match your role (or are universal fleet skills)
2. **Scripts / cron patterns** that improve reliability
3. **Config patterns** (approvals, compression, delegation, toolsets) worth copying
4. **Workflow conventions** (todos on GitHub, heartbeats, Discord routing)
5. **Mistakes / drift** (secrets nearly committed, n8n reintroduced, cloud crons against policy)
6. **McKing handoff** notes useful for later clone-scaffold

Write findings as:

```markdown
# Peer audit: <Reviewer> → <Subject> (YYYY-MM-DD)

## Steal / adopt (high value)
- ...

## Nice-to-have
- ...

## Do not copy (role mismatch or risk)
- ...

## Security notes
- ...

## Suggested concrete actions for <Subject>
1. ...
```

Save under **reviewer’s** or **subject’s** `git-safe/` as agreed; default:

`backup/<Subject>/git-safe/peer-audit-of-<Subject>-YYYY-MM-DD.md` authored by reviewer.

---

## 5. Apply phase

Subject agent:

1. Reads peer audit
2. Applies safe improvements (skills, docs, scripts, memory facts that are non-secret)
3. Writes `adopted-from-audit-YYYY-MM-DD.md` (adopted / deferred / rejected + why)
4. Pushes; thanks peer in Discord

**Ben remains decision-maker** for security, spending, and major architecture.

---

## 6. Cadence while Ben is away (6 weeks)

| When | Who | What |
|------|-----|------|
| ASAP once | Porsche + Doc | First git-safe export each |
| Within 48h of peer export | Peer | Write peer-audit doc |
| After audit | Owner | Adopt + report |
| Weekly (optional) | Both | Re-export if skills/config changed a lot |
| McKing online later | McKing | Join same protocol |

Cloud cron cost policy still applies: prefer local models / manual exports until local LLM fleet ready.

---

## 7. Discord coordination

- 1:1 agent work: `#porsche-garage` / `#doc-garage`
- Cross-agent audit handoff: `#tire-shop` with `@mentions` (needs `DISCORD_ALLOW_BOTS=mentions` where bot-to-bot is required)
- Ben always has veto on security-sensitive adoption

---

**Last updated:** 2026-07-11  
**Status:** Active for Porsche + Doc; McKing when online
