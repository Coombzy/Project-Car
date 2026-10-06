# Demo chat worker — Zone handoff

Paper until Zone deploys it. A docs merge or an HTML upload is not that deploy.

The contact page posts to same-origin `POST /api/demo-chat`. This worker is the only thing that calls Apex. The browser never sees a token.

## What is already in git

- `apps/website/html/contact.html` plus `demo-chat.js` / `demo-chat.css`. Zone Direct Upload of `apps/website/html` ships the widget. It shows “not connected” until this route exists.
- This directory is **not** part of that upload. Do not copy it into `html/`.

## What Zone does after the HTML is on `projectcar-brochure`

1. Deploy this directory as its **own** Worker (`wrangler.toml` name `projectcar-demo-chat`). Do not replace Worker `projectcar-brochure`.
2. Attach a route for **only** `/api/demo-chat` on `projectcar.ca` and `www.projectcar.ca`. Do not attach a catch-all. Brochure HTML stays on `projectcar-brochure`.
3. Set two secrets on this worker. Not in git.
   - `APEX_DEMO_GATEWAY_URL` — `https` origin only (`*.cursor.sh` or `*.cursor.com`). No path. Not a `cursorvm.com` host.
   - `APEX_DEMO_TOKEN` — a credential that can `sendPrompt` **only** to Apex `3f6c46ec-6dee-4c88-a3a5-6c7c1dbc6765`.
4. If the only token you have is the fleet gbot / Cursor session (the one that can message Lead, Chief, or Doc), **do not deploy**. Tell Lead. That token does not go on the public edge.

The bot id is fixed in code. The page cannot choose a different bot. The worker calls `sendPrompt` and `getAgentTranscriptTail` and no other gateway method. Apex’s thread is shared, so the worker returns only the assistant text whose id matches this visitor’s nonce. It drops every other entry. Do not turn on logging of those responses.

Apex stays demo-only: brochure and Soft-530, no fleet tools, refuse secrets. This worker cannot switch that off.

No Doc unfreeze. No shop-web change. No `/member` route.
