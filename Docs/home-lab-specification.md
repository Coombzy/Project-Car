# Home Lab Specification

**Last Updated:** 2026-08-12  
**Status:** Stub in this repo — restore the full July draft in a later pass  
**Canonical intent:** `Coombzy/Project-Car` → `Docs/home-lab-specification.md`

A longer draft still lives in the Hermes skill / Desktop copies. Until it is copied here and scrubbed, use these facts (they override older “Porsche hosts Nextcloud” language):

| Machine | Role now | Role later |
|---------|----------|------------|
| **Doc** (M1 Max, 64 GB) | Nextcloud 30, Vaultwarden, projectcar.ca origin | Inference / overflow |
| **McKing** (i9 + RTX 5080, 30–50 TB) | Not hosting the hub yet | Permanent hub, backups, GPU |
| **Porsche** (M4 Pro) | Travel client | Travel client — **not** the NC server |
| **Code Mater** | Discord field agent | Termux/SSH later |

Runtime path on Doc: `~/hermes-tools/mission-control`.  
Backups: `~/Desktop/Mission-Control/backups/nextcloud/`.  
Mesh: Tailscale. Public site: Cloudflare Tunnel → `:8088`.

Related: `mission-control-architecture.md`, `platform-architecture.md`, `Docs/nextcloud-progress.md`.
