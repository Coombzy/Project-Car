# Fleet mutual-audit — quick checklist

## Project Car Discord (Doc host)

| Entity | ID / name |
|--------|-----------|
| Guild | Project Car `1366682329623302214` |
| Doc bot | `1520953070866006176` |
| Porsche bot | `1519835415522185418` |
| Ben | `245025569337507841` |
| Shared floor | `#tire-shop` `1524975356656746547` |
| Doc home | `#doc-garage` `1524975085755170897` |

Ping Porsche: `<@1519835415522185418>`  
Send: `hermes send --to discord:#tire-shop "..."` or `discord:<channel_id>:<thread_id>`

## Default clone (Doc)

`/Users/dochak/hermes-tools/Automation`  
Remote: `https://github.com/Coombzy/Automation.git` (public)

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
- `backup/<Subject>/git-safe/peer-audit-of-<Subject>-YYYY-MM-DD.md`

Never: `~/.hermes/.env`, `auth.json`, profile tarballs, session DBs.

## Close-out message skeleton

```
**Doc status | mutual-audit** <@Porsche>

### Done
- inventory + AUDIT-PACK under backup/Doc/git-safe/
- peer-audit path
- commit SHA + push status (live URLs if pushed)

### Blocked (if any)
- exact error + one command Ben can run

### Next for peer
- reverse audit link
```
