"use server";

import { redirect } from "next/navigation";

import { parseApiError, shopApiUrl } from "../../lib/config";
import { extractMemberSessionValue } from "../../lib/session-cookie";
import { writeMemberSessionCookie } from "../../lib/session";

type SignupModeName = "self_serve" | "waitlist";

function readMode(body: unknown): SignupModeName | null {
  if (!body || typeof body !== "object" || !("mode" in body)) {
    return null;
  }
  const mode = (body as { mode?: unknown }).mode;
  switch (mode) {
    case "self_serve":
    case "waitlist":
      return mode;
    default:
      return null;
  }
}

async function readJson(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return null;
  }
}

function blank(value: FormDataEntryValue | null): string {
  return String(value ?? "").trim();
}

export async function signupAction(formData: FormData): Promise<void> {
  const tierName = blank(formData.get("tier_name")) || "basic";
  let response: Response;
  try {
    response = await fetch(`${shopApiUrl()}/signup`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: blank(formData.get("name")),
        email: blank(formData.get("email")),
        phone: blank(formData.get("phone")),
        password: String(formData.get("password") ?? ""),
        tier_name: tierName,
        notes: blank(formData.get("notes")),
      }),
      cache: "no-store",
    });
  } catch {
    redirect(`/signup?error=${encodeURIComponent("Could not sign up.")}`);
  }

  const body = await readJson(response);
  if (!response.ok) {
    const error = parseApiError(response.status, body, "Could not sign up.");
    redirect(`/signup?error=${encodeURIComponent(error.message)}`);
  }

  const mode = readMode(body);
  if (mode === null) {
    redirect("/signup?error=Could%20not%20start%20the%20session.");
  }
  switch (mode) {
    case "self_serve": {
      const token = extractMemberSessionValue(response.headers.getSetCookie());
      if (!token) {
        redirect("/signup?error=Could%20not%20start%20the%20session.");
      }
      await writeMemberSessionCookie(token);
      redirect("/member");
    }
    case "waitlist":
      redirect("/signup?joined=1");
    default: {
      const unexpected: never = mode;
      redirect(`/signup?error=${encodeURIComponent(String(unexpected))}`);
    }
  }
}
