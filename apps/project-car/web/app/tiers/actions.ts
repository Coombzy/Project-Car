"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError, parseApiError, shopApiUrl, SESSION_COOKIE } from "../../lib/config";
import { patchTier } from "../../lib/shop-api";
import { readSessionToken } from "../../lib/session";

export type PricingMultiplier = {
  id: string;
  label: string;
  multiplier: string;
  sort_order: number;
};

export type PricingSettings = {
  bands: PricingMultiplier[];
  overlays: PricingMultiplier[];
};

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

async function shopJson<T>(path: string, fallback: string, init: RequestInit = {}): Promise<T> {
  const token = await readSessionToken();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body !== undefined && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token && !headers.has("Cookie")) {
    headers.set("Cookie", `${SESSION_COOKIE}=${encodeURIComponent(token)}`);
  }
  let response: Response;
  try {
    response = await fetch(`${shopApiUrl()}${path}`, {
      ...init,
      headers,
      cache: "no-store",
    });
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, fallback);
  }
  return body as T;
}

export async function listPricingSettings(): Promise<PricingSettings> {
  return shopJson<PricingSettings>("/tiers/pricing", "Could not load band and overlay multipliers.");
}

export async function patchTierAction(formData: FormData): Promise<void> {
  const name = String(formData.get("name") ?? "");
  try {
    await patchTier(name, {
      display_name: String(formData.get("display_name") ?? ""),
      price: String(formData.get("price") ?? "0"),
      included_tokens: Number(formData.get("included_tokens") ?? 0),
      booking_window_days: Number(formData.get("booking_window_days") ?? 1),
      max_simultaneous_bookings: Number(formData.get("max_simultaneous_bookings") ?? 1),
      notes: String(formData.get("notes") ?? "") || null,
    });
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not save the tier.";
    redirect(`/tiers?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/tiers");
  redirect("/tiers");
}

export async function patchPricingAction(formData: FormData): Promise<void> {
  const bands: { id: string; multiplier: string }[] = [];
  const overlays: { id: string; multiplier: string }[] = [];
  for (const [key, value] of formData.entries()) {
    if (typeof value !== "string") {
      continue;
    }
    const multiplier = value.trim();
    if (key.startsWith("band:")) {
      bands.push({ id: key.slice("band:".length), multiplier });
    } else if (key.startsWith("overlay:")) {
      overlays.push({ id: key.slice("overlay:".length), multiplier });
    }
  }
  try {
    await shopJson("/tiers/pricing", "Could not save multipliers.", {
      method: "PATCH",
      body: JSON.stringify({ bands, overlays }),
    });
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not save multipliers.";
    redirect(`/tiers?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/tiers");
  redirect("/tiers");
}

export async function grantPeriodAllocationAction(): Promise<void> {
  let granted = 0;
  let skipped = 0;
  try {
    const result = await shopJson<{ granted?: unknown; skipped?: unknown }>(
      "/tiers/period-allocation/grant",
      "Could not grant this month's allotment.",
      { method: "POST" },
    );
    granted = Array.isArray(result.granted) ? result.granted.length : 0;
    skipped = typeof result.skipped === "number" ? result.skipped : 0;
  } catch (error) {
    const message =
      error instanceof ShopApiError ? error.message : "Could not grant this month's allotment.";
    redirect(`/tiers?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/tiers");
  redirect(`/tiers?granted=${granted}&skipped=${skipped}`);
}
