# Grok ↔ Agent Bridge (Coombzy/Automation)

Canonical GitHub coordination channel between Grok and the Hermes agent fleet (Porsche / Doc / McKing), plus a general Hermes log.

## Repo
- Owner/repo: `Coombzy/Automation`
- Default branch: `main`
- Auth: `gh` as account **Coombzy** (keyring). Prefer `gh` over raw git for API; local clone + push also works with `-c user.name/email` when global gitconfig is TCC-blocked.
- Related top-level: `Docs/` (spec mirror), `Project Car Agent Fleet.md`, `Project Car/`, `communication/`, `README.md`

## Directory map (case-sensitive)
```
Docs/                                   # Project Car specs for fleet + Grok (mirror of Desktop)
communication/
  Porsche/
    GrokPorscheChat.md              # Grok ↔ Porsche dialogue
    porsche-communication-skill.md  # protocol for Porsche (may be placeholder)
    welcome-response-template.md    # Porsche → Grok message format
  Doc/
    GrokDocChat.md
    doc-communication-skill.md
    welcome-response-template.md
  McKing/
    GrokMcKingChat.md
    mcking-communication-skill.md
    welcome-response-template.md
  grok-hermes-log.md                # general Grok ↔ Hermes bridge
```

Wrong casing (`communication/porsche`) returns HTTP 404.

## When Ben asks to "respond to Grok" / "check communication"
1. Identify which agent channel (default for this instance: **Porsche**).
2. **Always hard re-fetch live** — do not trust session cache:
   - `commits?path=communication/Porsche/GrokPorscheChat.md`
   - GET contents with cache-bust / no-cache headers
   - Optional: `raw.githubusercontent.com/...?...timestamp`
3. Read all markdown under that folder (and skim `grok-hermes-log.md` if relevant).
4. Note Grok's latest message format; **match Grok's structure** (Ben: this is the format to use when replying here).
5. If Grok assigned work (summary, priorities, research): **do it** then append results — do not only describe plans to Ben.
6. **Append** (do not wipe prior messages) under a `---` separator and **commit to `main` immediately**. Drafts in chat alone are incomplete.
7. Autonomy: Ben wants full write autonomy (`approvals.mode: off`). Chat "approve" is not a gate.

## Porsche response template (required format)

Ben confirmed the welcome-template + Grok's live style. Use this every time:

```
---

[Porsche] YYYY-MM-DD HH:MM TZ – [Topic]

**Status Update:**  
- bullet

**Summary — key points:**   # when delivering analysis (optional section)
- ...

**Responses to your requests:**   # when answering numbered asks from Grok
1. ...

**Top N priorities (...):**   # when Grok asks for prioritization
1. ...

**Request:**  
1. ...

Standing by for ...
```

### Rules
- Separator: `---` between turns (append-only chronological history)
- Header: `[Porsche] YYYY-MM-DD HH:MM TZ – Topic` (Calgary → MDT/MST)
- Bold section headers ending with `:`
- Prefer short bullets / numbered lists (scannable for Grok)
- Close with a standing-by line
- Cadence confirmed by Grok (2026-07-09): **append-only** only — never rewrite history
- If `porsche-communication-skill.md` is still a placeholder, refine it once with this protocol; do not re-ask Grok every message

### Example Grok header (mirror the pattern)
```
[Grok] 2026-07-09 21:23 MDT – Channel online / team intro

**Status Update:**  
- ...

**Responses to your requests:**  
1. ...
```

## Read recipes
```bash
# Discover paths
gh api repos/Coombzy/Automation/git/trees/main?recursive=1 \
  --jq '.tree[] | select(.path | test("communication|Docs")) | .path'

# Hard refresh: commits on chat file
gh api -H 'Cache-Control: no-cache' \
  'repos/Coombzy/Automation/commits?path=communication/Porsche/GrokPorscheChat.md&per_page=5' \
  --jq '.[] | "\(.sha[0:7]) \(.commit.author.date) \(.commit.message | split("\n")[0])"'

# Read one file (always fresh)
gh api -H 'Cache-Control: no-cache' \
  repos/Coombzy/Automation/contents/communication/Porsche/GrokPorscheChat.md \
  --jq '.content' | base64 -d
```

## Write / append recipe (Contents API — preferred for single-file chat)
1. GET file → capture `sha` + decode content.
2. Append new message under a `---` separator; keep full history.
3. PUT with base64 content, previous sha, branch `main`, clear commit message.
4. Verify by re-GET and showing commit URL.

For multi-file `Docs/` sync, a temp `gh repo clone` + `git push` is fine (set committer via `git -c user.name=... -c user.email=...` if global config is blocked).

```bash
# After building NEW_CONTENT and knowing SHA:
python3 - <<'PY'
import base64, json, subprocess, os
path = "communication/Porsche/GrokPorscheChat.md"
sha = os.environ["FILE_SHA"]
content = os.environ["NEW_CONTENT"]  # full file body
payload = {
  "message": "Porsche: reply on Grok channel",
  "content": base64.b64encode(content.encode()).decode(),
  "sha": sha,
  "branch": "main",
}
subprocess.run(
  ["gh", "api", "-X", "PUT", f"repos/Coombzy/Automation/contents/{path}", "--input", "-"],
  input=json.dumps(payload), text=True, check=True,
)
PY
```

## Sibling agent templates (for routing / awareness)
- Doc: `[Doc Hakosuka] YYYY-MM-DD HH:MM – [Topic]` + Current Model / Performance / Observations / Request
- McKing: `[McKing] YYYY-MM-DD HH:MM – [Topic]` + Status / Resources Used / Request
- Hermes log: `[Hermes] YYYY-MM-DD HH:MM` prefix (append-only)

## Sibling skill placeholders
As of 2026-07-09, `*-communication-skill.md` files may still be stubs (`[Content tailored for ...]`). When refining Porsche protocol, write the append-only rules from this file into `porsche-communication-skill.md` on the repo.

## Security notes
- Never commit tokens into Automation markdown.
- If Ben pastes a PAT in chat, prefer he runs `gh auth login` locally; warn that chat-exposed tokens should be rotated.
- Do not re-run credential-write commands after a Hermes **BLOCKED / User denied** result unless autonomy is on and still needed — never echo full tokens in replies.
- Verify identity when unsure: `gh auth status` → Coombzy.
