import {
  APEX_AGENT_ID,
  allowedGatewayOrigin,
  allowedPageOrigin,
  cleanVisitorMessage,
  demoPrompt,
  pickReply,
  scrubReply,
} from "./reply.js";

const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 6;
const POLL_TIMES = 12;
const POLL_MS = 800;
const hits = new Map();

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function clientIp(request) {
  return request.headers.get("cf-connecting-ip") || "unknown";
}

function limited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= MAX_PER_WINDOW) {
    hits.set(ip, recent);
    return true;
  }
  recent.push(now);
  hits.set(ip, recent);
  return false;
}

async function gateway(origin, token, method, body) {
  const response = await fetch(`${origin}/api/${method}`, {
    method: "POST",
    redirect: "error",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) return null;
  return response.json();
}

async function waitForReply(origin, token, nonce) {
  for (let i = 0; i < POLL_TIMES; i += 1) {
    if (i > 0) await new Promise((resolve) => setTimeout(resolve, POLL_MS));
    const data = await gateway(origin, token, "getAgentTranscriptTail", {
      id: APEX_AGENT_ID,
      limit: 8,
    });
    if (!data) return { error: "upstream" };
    const entries = Array.isArray(data.entries)
      ? data.entries
      : data.transcript && Array.isArray(data.transcript.entries)
        ? data.transcript.entries
        : [];
    const reply = scrubReply(pickReply(entries, nonce));
    if (reply) return { reply };
  }
  return { error: "timeout" };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/demo-chat") return json(404, { error: "not_found" });
    if (request.method !== "POST") return json(405, { error: "method" });
    if (!allowedPageOrigin(request.headers.get("origin") || "")) {
      return json(403, { error: "origin" });
    }
    if (limited(clientIp(request))) return json(429, { error: "busy" });

    const origin = allowedGatewayOrigin(env.APEX_DEMO_GATEWAY_URL);
    const token = typeof env.APEX_DEMO_TOKEN === "string" ? env.APEX_DEMO_TOKEN.trim() : "";
    if (!origin || !token) return json(503, { error: "not_connected" });

    let payload;
    try {
      const raw = await request.text();
      if (raw.length > 2000) return json(413, { error: "too_large" });
      payload = JSON.parse(raw);
    } catch {
      return json(400, { error: "bad_json" });
    }
    const message = cleanVisitorMessage(payload && payload.message);
    if (!message) return json(400, { error: "bad_message" });

    const nonce = crypto.randomUUID();
    const sent = await gateway(origin, token, "sendPrompt", {
      agentId: APEX_AGENT_ID,
      prompt: demoPrompt(message),
      clientNonce: nonce,
    });
    if (!sent || sent.accepted === false) return json(502, { error: "not_sent" });

    const result = await waitForReply(origin, token, nonce);
    if (result.reply) return json(200, { reply: result.reply });
    if (result.error === "timeout") return json(504, { error: "no_reply" });
    return json(502, { error: "not_sent" });
  },
};
