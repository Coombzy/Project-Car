"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { notifyFill } from "../../lib/shop-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Fill notify failed.";
  redirect(`/fill?error=${encodeURIComponent(message)}`);
}

export async function notifyFillAction(formData: FormData): Promise<void> {
  const dryRun = String(formData.get("mode") ?? "dry_run") !== "send";
  const discount = String(formData.get("discount_pct") ?? "").trim();
  const channels = ["email", "sms", "push"].filter((channel) => formData.get(channel) === "on");
  try {
    await notifyFill({
      dry_run: dryRun,
      discount_pct: discount || undefined,
      channels: channels.length ? channels : ["email"],
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/fill");
  revalidatePath("/schedule");
  revalidatePath("/member/schedule");
  const notice = dryRun ? "dry-run queued in the outbox" : "fill offer published and notices sent";
  redirect(`/fill?notice=${encodeURIComponent(notice)}`);
}
