#!/usr/bin/env python3
"""Apex — Project Car public community chat agent (xAI Grok)."""
from __future__ import annotations

import json
import os
import re
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = os.environ.get("APEX_HOST", "0.0.0.0")
PORT = int(os.environ.get("APEX_PORT", "8090"))
MODEL = os.environ.get("APEX_MODEL", "grok-4.5")
AUTH_FILE = Path(os.environ.get("APEX_AUTH_FILE", "/auth/auth.json"))
LOG_DIR = Path(os.environ.get("APEX_LOG_DIR", "/app/logs"))
MAX_HISTORY = 12
MAX_USER_CHARS = 2000
RATE_LIMIT = 30  # messages per session per hour

SYSTEM_PROMPT = """You are Apex, Project Car's public community and marketing agent.

## Who you are
- Friendly, clear, practical — not hype-driven or salesy.
- You help visitors understand the Project Car vision and how to get involved.
- You speak as Apex (first person is fine: "I can help with…").

## What Project Car is (public facts you may use)
- Project Car is a 24/7, community-driven maker-space style automotive shop.
- Focus: custom mechanical and fabrication work on project vehicles.
- Positioning: Community driven, Automotive Maker Space.
- We provide space, tools, skills, and knowledge to help people make their dream car a reality.
- Standout directions (concept / planned — not a claim of full open operations today):
  - 24/7 shop access
  - Full fabrication tools
  - Individual work bays with 2-post hoists
  - Community expertise and project support
  - Project planning and mechanical, electrical, and fabrication mentorship
- Public site: https://projectcar.ca — currently early build ("Project Underway").
- Human contact: info@projectcar.ca
- Website progress is early (~10% on the public page).

## Hard guardrails (never break these)
1. ONLY discuss Project Car topics: shop concept, maker-space model, tools/facilities concept, membership direction (high level), public roadmap/vision, how to get involved, website feedback.
2. Do NOT invent details that have not been published (no fake prices, hours schedule, address, inventory lists, opening date, member counts, legal entity details, etc.).
3. Do NOT discuss finances, legal matters, private internal systems (Mission Control, Vaultwarden internals, agent infrastructure, servers, APIs, keys), member/personal data, or unreleased private plans.
4. Never claim the shop is fully open or fully operational — it is in early build / project underway.
5. If you do not know, or the question is out of scope, say so clearly and direct them to email info@projectcar.ca.
6. Keep answers concise (usually a short paragraph or a few bullets). Invite email for anything that needs a human.
7. You may acknowledge feedback and thank people; do not promise specific features or timelines unless published above.
8. Stay in character as Apex.

## When unsure
Say you don't have that published yet and suggest writing info@projectcar.ca.
"""

QUESTION_RE = re.compile(
    r"\?|^\s*(how|what|when|where|why|who|which|can|do|does|is|are|will|would|could|should)\b",
    re.I,
)
FEEDBACK_RE = re.compile(
    r"\b(feedback|suggest|suggestion|advice|recommend|improve|consider|idea|wish|should|feature request|bug|confusing|love|hate|prefer)\b",
    re.I,
)

# session_id -> list of timestamps
_rate: dict[str, list[float]] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_access_token() -> str:
    env_tok = os.environ.get("APEX_XAI_TOKEN") or os.environ.get("XAI_API_KEY")
    if env_tok:
        return env_tok.strip()
    if not AUTH_FILE.is_file():
        raise RuntimeError(f"auth file missing: {AUTH_FILE}")
    data = json.loads(AUTH_FILE.read_text())
    providers = data.get("providers") or {}
    xai = providers.get("xai-oauth") or {}
    tokens = xai.get("tokens") or {}
    tok = tokens.get("access_token")
    if tok:
        return tok
    pool = (data.get("credential_pool") or {}).get("xai-oauth") or []
    if pool and pool[0].get("access_token"):
        return pool[0]["access_token"]
    raise RuntimeError("no xAI access token available")


def classify_user_text(text: str) -> dict:
    return {
        "is_question": bool(QUESTION_RE.search(text)),
        "is_feedback": bool(FEEDBACK_RE.search(text)),
    }


def should_log_user(text: str, flags: dict) -> bool:
    return bool(flags.get("is_question") or flags.get("is_feedback") or len(text.strip()) >= 12)


def append_jsonl(path: Path, row: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def log_event(row: dict) -> None:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    append_jsonl(LOG_DIR / f"apex-{day}.jsonl", row)
    # Convenience feed for FAQ mining
    if row.get("role") == "user" and row.get("logworthy"):
        append_jsonl(LOG_DIR / "feedback-and-questions.jsonl", row)


def rate_ok(session_id: str) -> bool:
    now = time.time()
    window = 3600.0
    bucket = _rate.setdefault(session_id, [])
    _rate[session_id] = [t for t in bucket if now - t < window]
    if len(_rate[session_id]) >= RATE_LIMIT:
        return False
    _rate[session_id].append(now)
    return True


def call_xai(messages: list[dict]) -> str:
    token = load_access_token()
    body = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 700,
    }
    req = urllib.request.Request(
        "https://api.x.ai/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "project-car-apex/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"xAI HTTP {e.code}: {err_body}") from e
    choices = payload.get("choices") or []
    if not choices:
        raise RuntimeError("xAI returned no choices")
    return (choices[0].get("message") or {}).get("content") or ""


def normalize_history(raw) -> list[dict]:
    out = []
    if not isinstance(raw, list):
        return out
    for item in raw[-MAX_HISTORY:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = (item.get("content") or "").strip()
        if role not in ("user", "assistant") or not content:
            continue
        out.append({"role": role, "content": content[:MAX_USER_CHARS]})
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "Apex/1.0"

    def log_message(self, fmt, *args):
        # quieter access log
        pass

    def _cors(self):
        origin = self.headers.get("Origin", "")
        # Same-origin via nginx preferred; allow local dev hosts
        allow = "*"
        if origin:
            allow = origin
        self.send_header("Access-Control-Allow-Origin", allow)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Vary", "Origin")

    def _json(self, code: int, obj: dict):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ("/health", "/healthz", "/api/apex/health"):
            ok = True
            detail = "ok"
            try:
                load_access_token()
            except Exception as e:
                ok = False
                detail = str(e)
            return self._json(200 if ok else 503, {"status": "ok" if ok else "degraded", "model": MODEL, "auth": detail})
        return self._json(404, {"error": "not_found"})

    def do_POST(self):
        if self.path not in ("/chat", "/api/apex/chat"):
            return self._json(404, {"error": "not_found"})
        try:
            length = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            length = 0
        if length <= 0 or length > 100_000:
            return self._json(400, {"error": "bad_request"})
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return self._json(400, {"error": "invalid_json"})

        session_id = (payload.get("session_id") or "").strip() or str(uuid.uuid4())
        user_message = (payload.get("message") or "").strip()
        history = normalize_history(payload.get("history"))

        if not user_message:
            return self._json(400, {"error": "empty_message", "session_id": session_id})
        if len(user_message) > MAX_USER_CHARS:
            user_message = user_message[:MAX_USER_CHARS]

        if not rate_ok(session_id):
            return self._json(
                429,
                {
                    "error": "rate_limited",
                    "reply": "You're sending messages a bit quickly. Please wait a moment, or email info@projectcar.ca.",
                    "session_id": session_id,
                },
            )

        flags = classify_user_text(user_message)
        logworthy = should_log_user(user_message, flags)
        log_event(
            {
                "ts": utc_now(),
                "session_id": session_id,
                "role": "user",
                "content": user_message,
                "logworthy": logworthy,
                **flags,
                "history_tail": history[-4:],
            }
        )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        try:
            reply = call_xai(messages).strip()
            if not reply:
                raise RuntimeError("empty model reply")
        except Exception as e:
            log_event(
                {
                    "ts": utc_now(),
                    "session_id": session_id,
                    "role": "error",
                    "content": str(e)[:500],
                }
            )
            reply = (
                "I'm having trouble responding right now. "
                "Please email info@projectcar.ca and the team will get back to you."
            )
            return self._json(200, {"reply": reply, "session_id": session_id, "degraded": True})

        log_event(
            {
                "ts": utc_now(),
                "session_id": session_id,
                "role": "assistant",
                "content": reply,
                "model": MODEL,
            }
        )
        return self._json(200, {"reply": reply, "session_id": session_id, "model": MODEL})


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"apex listening on {HOST}:{PORT} model={MODEL}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
