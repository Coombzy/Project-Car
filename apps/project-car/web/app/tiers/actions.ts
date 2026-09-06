"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { patchTier } from "../../lib/shop-api";

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
