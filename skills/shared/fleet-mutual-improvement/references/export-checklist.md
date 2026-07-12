# Fleet mutual-improvement — export checklist (absorbed from fleet-mutual-audit)

Canonical runbook is **`fleet-mutual-improvement`**. This file holds the mechanical export checklist so we do **not** dual-run `fleet-mutual-audit`.

## Project Car Discord (public IDs)

| Entity | ID / name |
|--------|-----------|
| Guild | Project Car `1366682329623302214` |
| Porsche bot | `1519835415522185418` |
| Doc bot | `1520953070866006176` |
| Ben | `245025569337507841` |
| Shared floor | `#tire-shop` `1524975356656746547` |
| Porsche home | `#porsche-garage` `1519854154699378868` |
| Doc home | `#doc-garage` `1524975085755170897` |

Ping peers with real `<@bot_id>`. From non-home sessions: `hermes send --to discord:#tire-shop "..."`.

## Default clones

| Agent | Typical Automation clone |
|-------|--------------------------|
| Porsche | `~/Documents/Automation` |
| Doc | `/Users/dochak/hermes-tools/Automation` (may vary) |

Remote: `https://github.com/Coombzy/Automation.git` (public).

## Inventory fields (minimum)

- agent, agent_display_name, machine_role, profile
- exported_at (UTC ISO), export_kind, repo_note
- hardware: chip, memory_gb, cores_note, model_identifier, os, hostname_public (**no serial**)
- hermes version + install_dir
- skills_count + skills[] {path, name, description[:220], bytes}
- config_top_level_keys + config_redacted
- scripts[], cron {jobs/purposes only}
- memory_summary {name, bytes, sha256_16, preview_lines≤3}
- local_llm (ollama list with timeout)
- discord_role_notes
- routing preference string (host-sized)

## Redaction

- Key name matches `key|token|secret|password|api_key|auth|credential|private|bot_token` → value `<redacted>` unless empty/bool/0
- Values matching `sk-|ghp_|gho_|xox|Bearer |-----BEGIN` → `<redacted>`
- Long strings >400 chars truncated in redacted tree

## External probes

| Probe | Timeout |
|-------|---------|
| ollama list | 5s |
| hermes --version | 10s |
| sw_vers / which | 2–3s |

On timeout: store literal timeout string; continue export.

## Commit scope

Only:

- `backup/<Agent>/git-safe/**`
- peer-audit / recommendations / adoption notes under git-safe
- skill catalogs / published when part of same session (optional)

Never: `~/.hermes/.env`, `auth.json`, profile tarballs, session DBs, security-audit reports with serials.

## Close-out message skeleton

```
**FLEET_MUTUAL_IMPROVEMENT** | <You> | YYYY-MM-DD
- Export: OK
- Adopted: N items (one-liners)
- Rejected for role-lock: …
- Recommendations for <Peer>: path
- Divergence: healthy | warning
- Commit: <sha>
```
