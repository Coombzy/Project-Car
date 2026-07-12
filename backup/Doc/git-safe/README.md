# Doc Hakosuka git-safe manifests

Export **sanitized** inventory here for mutual audit with Porsche (and later McKing).

See `../../MUTUAL-AUDIT-PROTOCOL.md`.

## Doc: first export (when online)

On Doc machine:

```bash
cd ~/Documents/Automation   # or your clone path
git pull

# Then either:
# 1) Ask Doc Hermes: "Generate git-safe mutual-audit pack into backup/Doc/git-safe per MUTUAL-AUDIT-PROTOCOL"
# 2) Or run a local inventory script mirroring Porsche's export

git add backup/Doc/git-safe backup/MUTUAL-AUDIT-PROTOCOL.md
git commit -m "Doc git-safe mutual-audit inventory"
git push
```

**Never** commit `.env`, `auth.json`, or full profile tarballs.
