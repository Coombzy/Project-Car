"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { SESSION_COOKIE, ShopApiError, parseApiError, shopApiUrl } from "../../lib/config";
import { readSessionToken } from "../../lib/session";
import { markWaitlistContacted, setSignupMode } from "../../lib/shop-api";

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

export async function setSignupModeAction(formData: FormData): Promise<void> {
  const mode = String(formData.get("mode") ?? "");
  if (mode !== "self_serve" && mode !== "waitlist") {
    redirect("/waitlist?error=Signup%20mode%20must%20be%20self-serve%20or%20the%20waitlist%20fallback.");
  }
  try {
    await setSignupMode(mode);
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not save signup mode.";
    redirect(`/waitlist?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/waitlist");
  revalidatePath("/signup");
  redirect("/waitlist");
}

export async function markContactedAction(formData: FormData): Promise<void> {
  try {
    await markWaitlistContacted(String(formData.get("id") ?? ""));
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not mark contacted.";
    redirect(`/waitlist?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/waitlist");
  revalidatePath("/");
  redirect("/waitlist");
}

export async function convertWaitlistAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  const tierName = String(formData.get("tier_name") ?? "");
  try {
    const token = await readSessionToken();
    const headers = new Headers({
      Accept: "application/json",
      "Content-Type": "application/json",
    });
    if (token) {
      headers.set("Cookie", `${SESSION_COOKIE}=${encodeURIComponent(token)}`);
    }
    let response: Response;
    try {
      response = await fetch(`${shopApiUrl()}/waitlist/${id}/convert`, {
        method: "POST",
        headers,
        body: JSON.stringify({ tier_name: tierName }),
        cache: "no-store",
      });
    } catch {
      throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
    }
    const body = await readJson(response);
    if (!response.ok) {
      throw parseApiError(response.status, body, "Could not convert the waitlist row.");
    }
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not convert the waitlist row.";
    redirect(`/waitlist?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/waitlist");
  revalidatePath("/members");
  revalidatePath("/");
  redirect("/waitlist");
}
