# AI stack surface checklist (Hermes + Ollama + local models)

## Ollama
- **Bind:** must be `127.0.0.1:11434` (and helper localhost ports). Flag any `*:11434` / `0.0.0.0`.
- Never put raw Ollama on Tailscale/LAN without an auth reverse proxy.
- `OLLAMA_NO_CLOUD=0` means cloud features allowed — set `1` for offline-only preference.
- Models on disk are large; permissions under Ollama library should stay user-private.

## Hermes (`~/.hermes`)
| Path | Expected perms |
|---|---|
| `~/.hermes/` | `700` |
| `.env`, `auth.json`, `config.yaml` | `600` |
| `state.db`, `state.db-*` | `600` (often wrongly `644`) |
| `logs/*.log` | `600` (often wrongly `644`) |
| `sessions/` | `700`, dumps `600` |

- Redact when auditing config: print structure/key names, not API tokens.
- `terminal.backend: local` + full tools = high blast radius under prompt injection — use `secure-ai` profile for untrusted content.
- Prefer hard tool-loop stops for risky sessions.
- Custom local provider example: `http://127.0.0.1:11434/v1` with local model name only.

## Routing (capability vs exposure)
- Cloud flagship (Grok) for plan/review: secrets leave the machine via provider API — expected for that path.
- Local Qwen/Gemma for implement: keeps code on-box; still can read repo via agent tools.
- Don’t log raw secrets into Hermes memory or SOUL.md.

## Backups
- No Time Machine = high impact for ransomware/agent `rm` mistakes.
- Back up `~/.hermes` (exclude huge caches/models_dev dumps if needed) + critical repos.
- Encrypted destination preferred.

## Firewall interaction
- Stale allows for `/usr/bin/python3` or agent interpreters mean a malicious listener won’t be blocked — prune allowlist after audits.
