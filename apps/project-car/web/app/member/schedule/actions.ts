"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { cancelMemberBooking, confirmMemberBooking, createMemberBooking } from "../../../lib/shop-api";

function weekTarget(formData: FormData): string {
  const week = String(formData.get("week") ?? "");
  return week ? `/member/schedule?week=${encodeURIComponent(week)}` : "/member/schedule";
}

function fail(formData: FormData, error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Booking action failed.";
  const base = weekTarget(formData);
  const sep = base.includes("?") ? "&" : "?";
  redirect(`${base}${sep}error=${encodeURIComponent(message)}`);
}

export async function memberCreateBookingAction(formData: FormData): Promise<void> {
  try {
    const created = await createMemberBooking({
      hoist_id: String(formData.get("hoist_id") ?? ""),
      start_at: String(formData.get("start_at") ?? ""),
      end_at: String(formData.get("end_at") ?? ""),
      notes: String(formData.get("notes") ?? "") || null,
    });
    await confirmMemberBooking(created.id);
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(weekTarget(formData));
}

export async function memberConfirmBookingAction(formData: FormData): Promise<void> {
  try {
    await confirmMemberBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(weekTarget(formData));
}

export async function memberCancelBookingAction(formData: FormData): Promise<void> {
  try {
    await cancelMemberBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(weekTarget(formData));
}
