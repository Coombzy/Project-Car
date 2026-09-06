"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import {
  cancelBooking,
  checkInBooking,
  completeBooking,
  confirmBooking,
  createBooking,
} from "../../lib/shop-api";

function weekTarget(formData: FormData): string {
  const week = String(formData.get("week") ?? "");
  return week ? `/schedule?week=${encodeURIComponent(week)}` : "/schedule";
}

function fail(formData: FormData, error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Booking action failed.";
  const base = weekTarget(formData);
  const sep = base.includes("?") ? "&" : "?";
  redirect(`${base}${sep}error=${encodeURIComponent(message)}`);
}

export async function createBookingAction(formData: FormData): Promise<void> {
  try {
    await createBooking({
      member_id: String(formData.get("member_id") ?? ""),
      hoist_id: String(formData.get("hoist_id") ?? ""),
      start_at: String(formData.get("start_at") ?? ""),
      end_at: String(formData.get("end_at") ?? ""),
      tokens: String(formData.get("tokens") ?? "1"),
      notes: String(formData.get("notes") ?? "") || null,
    });
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(weekTarget(formData));
}

export async function confirmBookingAction(formData: FormData): Promise<void> {
  try {
    await confirmBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(weekTarget(formData));
}

export async function checkInBookingAction(formData: FormData): Promise<void> {
  try {
    await checkInBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(weekTarget(formData));
}

export async function completeBookingAction(formData: FormData): Promise<void> {
  try {
    await completeBooking(String(formData.get("id") ?? ""), String(formData.get("unused_tokens") ?? "0"));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(weekTarget(formData));
}

export async function cancelBookingAction(formData: FormData): Promise<void> {
  try {
    await cancelBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(weekTarget(formData));
}
