# Adopted from audit — Porsche (2026-07-11)

**Owner:** Porsche  
**Source audits:**
- Porsche → Doc: `backup/Doc/git-safe/peer-audit-of-Doc-2026-07-11.md` (`f7e6e16`)
- Doc → Porsche: `backup/Porsche/git-safe/peer-audit-of-Porsche-2026-07-11.md` (`b798c58`)
- Doc adopt (partial): `backup/Doc/git-safe/adopted-from-audit-2026-07-11.md` (`5c2797c`)

**Policy:** Ben remains decision-maker on security, spend, and major architecture. No secrets entered public git.

---

## Adopted

| Item | Action taken | Notes |
|------|----------------|-------|
| `macos-security-hardening` | Installed under `~/.hermes/skills/productivity/` | Prefer Doc’s published tree from `skills-share/Doc/` (synced) |
| `xai-model-selection` | Installed under `~/.hermes/skills/mlops/` | SuperGrok Heavy = tier not model id |
| `grok` | Installed under `~/.hermes/skills/autonomous-ai-agents/` | Grok Build CLI delegation |
| `sqlalchemy-domain-modeling` | Installed under `~/.hermes/skills/software-development/` | Domain ORM patterns for Project Car |
| Architect-cloud / implement-local **policy** | Affirmed (MEMORY + skill) | Plan on Grok; bulk local only with **24GB-safe** models (not Doc’s 35B defaults) |
| Job-scoped stay-awake doctrine | Affirmed | Prefer `caffeinate` for long jobs; AlDente ~60% always-plugged hold unchanged |
| Discord routing | Already aligned | `require_mention` + inline bot mention + `#tire-shop` `no_thread_channels` |
| Inventory shape | Re-exported git-safe inventory | Doc-quality fields: hardware, local_llm, always_on_notes, discord_role_notes (no serials) |
| Outbound skill share for Doc | `skills-share/Porsche/` + tarball | Unblocks Doc ordered install |
| Backup script git-safe copy | `backup/Porsche/git-safe/scripts/daily-porsche-backup.sh` | Mirror of Doc’s script-share pattern |

## Skills count

- Before mutual-audit adopt: **96**
- After (+4 Doc skills): **100**

## Deferred

| Item | Why |
|------|-----|
| Doc’s dual 26B/35B Ollama set on Porsche | **24GB M4 Pro** — RAM mismatch; policy only |
| Wire `custom_providers` → Ollama now | Ollama.app may be present; list/timeout flaky at audit; enable when Ben wants local bulk on Porsche |
| Expose local LLM beyond localhost | Needs hardening + Ben OK |
| Kanban skills → Doc | Optional later |
| Amphetamine on Doc | Ben software baseline |
| Doc `approvals.mode` | Ben confirm; Porsche already autonomy-on |

## Rejected / will not copy

| Item | Why |
|------|-----|
| Doc as second PA | Role mismatch |
| 35B as Porsche default local model | RAM mismatch |
| Secrets / full profile tarballs into public git | Protocol ban |
| Blind skill-count parity | Only role-fit adoptions |

## Shared outbound (Porsche → Doc)

```text
skills-share/Porsche/autonomous-ai-agents/project-car/
skills-share/Porsche/autonomous-ai-agents/token_preflight/
skills-share/Porsche/autonomous-ai-agents/token_optimizer/
skills-share/Porsche/hermes-multi-agent-backup/
skills-share/Porsche/software-development/mission-control-development-heartbeat/
skills-share/Porsche/porsche-skills-for-doc-2026-07-11.tar.gz
backup/Porsche/git-safe/scripts/daily-porsche-backup.sh
```

### Doc install (ordered)

```bash
CLONE="${AUTOMATION_CLONE:-$HOME/hermes-tools/Automation}"
git -C "$CLONE" pull --ff-only

# Option A — tree copy (order = priority)
cp -R "$CLONE/skills-share/Porsche/autonomous-ai-agents/project-car" \
  ~/.hermes/skills/autonomous-ai-agents/
cp -R "$CLONE/skills-share/Porsche/autonomous-ai-agents/token_preflight" \
  ~/.hermes/skills/autonomous-ai-agents/
cp -R "$CLONE/skills-share/Porsche/autonomous-ai-agents/token_optimizer" \
  ~/.hermes/skills/autonomous-ai-agents/
cp -R "$CLONE/skills-share/Porsche/hermes-multi-agent-backup" \
  ~/.hermes/skills/
mkdir -p ~/.hermes/skills/software-development
cp -R "$CLONE/skills-share/Porsche/software-development/mission-control-development-heartbeat" \
  ~/.hermes/skills/software-development/

# Option B — tarball
tar -xzf "$CLONE/skills-share/Porsche/porsche-skills-for-doc-2026-07-11.tar.gz" \
  -C ~/.hermes/skills
```

Then Doc amends `adopted-from-audit-2026-07-11.md` and re-exports inventory once.

## Ops verification (Porsche host)

- [x] Four Doc skills present under `~/.hermes/skills/`
- [x] Secret scan clean on skill-share before push
- [x] Porsche skill-share trees + tarball staged
- [x] Inventory re-export with Doc-quality fields
- [x] Discord routing correct
- [x] GitHub write as Coombzy works
- [ ] Optional: small Ollama model later (not blocking)

## Mutual-audit loop status

| Side | Export | Peer audit | Adopt notes | Skill-share out |
|------|--------|------------|-------------|-----------------|
| Porsche | ✅ | ✅ | ✅ (this file) | ✅ |
| Doc | ✅ | ✅ | ✅ partial → complete after install | ✅ |

**Next:** Doc installs Porsche skill-share, amends adoption file, one inventory re-export. No further audit churn unless skills/config change materially.

**Status:** Porsche adopt phase **complete** for inbound Doc skills + outbound share.
