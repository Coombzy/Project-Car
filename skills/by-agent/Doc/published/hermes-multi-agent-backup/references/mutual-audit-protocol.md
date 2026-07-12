# Mutual agent audit protocol (fleet)

**Repo assumption:** `Coombzy/Automation` (or any fleet mirror) may be **public**. Treat every committed file as world-readable.

**Canonical live copy:** also under `Automation/backup/MUTUAL-AUDIT-PROTOCOL.md` when repo is available — keep skill reference and repo in sync when editing.

## Export checklist (each agent, on its own machine)

1. `git pull` Automation (or equivalent).
2. Build inventory into `backup/<Agent>/git-safe/`:
   - skills inventory
   - redacted config structure
   - non-secret scripts
   - cron schedule purposes
   - role / hardware / home channel
   - sanitized memory previews or hashes only
3. Write `AUDIT-PACK.md` (strengths + gaps / wants from peers).
4. Commit **only** `git-safe/` + protocol docs. Push.
5. Ping peer in `#tire-shop` with literal `<@peer_bot_id>`: “git-safe export ready.”

## Peer audit

Save as `backup/<Subject>/git-safe/peer-audit-of-<Subject>-YYYY-MM-DD.md` (reviewer authors).

Template sections:
- Steal / adopt (high value)
- Nice-to-have
- Do not copy (role mismatch or risk)
- Security notes
- Suggested concrete actions for subject

## Apply

Subject writes `adopted-from-audit-YYYY-MM-DD.md` and pushes. Ben vetoes security-sensitive adoption.

## What not to put on git

`.env`, `auth.json`, OAuth tokens, Discord bot tokens, full `hermes profile export` archives, private chat session DBs, detailed compromise/2FA recovery notes, private keys.

## Example strengths split (fleet roles)

| Agent | Typical steal-from |
|-------|--------------------|
| Porsche | GitHub todos source of truth, heartbeat/MC loop, fleet backup split, Discord-first ops, access policy, shopping CAD conventions |
| Doc | MLX/Ollama/local heavy-model workflows, long research patterns, always-on/sleep tricks, token/cost guardrails |
| McKing | GPU/CUDA coding toolchain, bulk storage receive-end, homelab compose (later) |

## Silent peer after brief

If peer only 👀: assume turn started then stalled. Probe with human @ + one-word alive token; re-send **short** HANDOFF; put bulk work in git, not Discord walls of text.
