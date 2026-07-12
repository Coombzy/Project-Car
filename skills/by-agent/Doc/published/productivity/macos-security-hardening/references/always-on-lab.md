# Doc always-on lab security appendix (M1 Max 64GB)

Threat bias: **local API exposure, long-lived agent tools, large model disk privacy, residual shop tools** — not Porsche travel-host hotel paranoia as the default workflow.

## Doc checklist (every audit)

1. **Ollama bind** — API must stay `127.0.0.1` only. Never `0.0.0.0` / LAN / raw Tailscale without auth reverse proxy.
   ```bash
   # examples of checks (adapt to install)
   lsof -iTCP -sTCP:LISTEN -P -n | grep -i ollama || true
   # config often: OLLAMA_HOST=127.0.0.1:11434
   ```
2. **Hermes perms** — `chmod 700 ~/.hermes`; secrets/DB/config/logs `600` where appropriate.
3. **Stay-awake** — **Amphetamine installed + running** (Ben confirmed 2026-07-12). Keep session active for gateway + long model jobs. Remaining baseline: battery app (coconutBattery / AlDente if laptop) — see `communication/Doc/Doc-Todo.md`.
4. **Single Tailscale** — App stack preferred; stop Homebrew userspace duplicate.
5. **Model disk privacy** — model weights + caches are large; keep on encrypted volume (FileVault); do not sync secrets into public git with inventories.
6. **Long-lived tool blast radius** — supervise destructive shell; prefer `secure-ai` profile for high-risk experiments.
7. **Used-Mac residue** — admin group, `sharing -l`, PhoneCheck/MacDiag TCC (Doc host was refurbished — residual hygiene normal).

## Low-risk auto-fix when autonomy on

- Hermes dir/file perms (`700`/`600`)
- Ollama localhost bind check + report
- Homebrew analytics off if still on

## Still Ben-gated (never silent)

- Firewall global on/off, stealth
- SIP, FileVault, Remote Login, Screen Sharing
- Firewall app allowlist removals that may break needed tools
- Lockdown Mode

## Report

Write `~/Desktop/macOS-Security-Audit-YYYY-MM-DD.md` — **no serials/UUIDs** in public `Coombzy/Automation` commits.
