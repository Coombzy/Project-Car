"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { markWaitlistContacted } from "../../lib/shop-api";

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
