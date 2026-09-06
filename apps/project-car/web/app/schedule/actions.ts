"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { scheduleHref, type ScheduleView } from "../../lib/calendar";
import {
  cancelBooking,
  checkInBooking,
  completeBooking,
  confirmBooking,
  createBooking,
} from "../../lib/shop-api";

function scheduleTarget(formData: FormData): string {
  const view = String(formData.get("view") ?? "");
  const week = String(formData.get("week") ?? "");
  const month = String(formData.get("month") ?? "");
  const hoist = String(formData.get("hoist") ?? "");
  return scheduleHref("/schedule", {
    view: view === "week" || view === "month" ? (view as ScheduleView) : undefined,
    week: week || undefined,
    month: month || undefined,
    hoist: hoist || undefined,
  });
}

function fail(formData: FormData, error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Booking action failed.";
  redirect(scheduleHref("/schedule", {
    view: String(formData.get("view") ?? "") === "week" ? "week" : "month",
    week: String(formData.get("week") ?? "") || undefined,
    month: String(formData.get("month") ?? "") || undefined,
    hoist: String(formData.get("hoist") ?? "") || undefined,
    error: message,
  }));
}

export async function createBookingAction(formData: FormData): Promise<void> {
  try {
    const kind = String(formData.get("kind") ?? "customer");
    const memberId = String(formData.get("member_id") ?? "").trim();
    await createBooking({
      member_id: kind === "shop" ? memberId || null : memberId,
      hoist_id: String(formData.get("hoist_id") ?? ""),
      start_at: String(formData.get("start_at") ?? ""),
      end_at: String(formData.get("end_at") ?? ""),
      notes: String(formData.get("notes") ?? "") || null,
      kind,
    });
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}

export async function confirmBookingAction(formData: FormData): Promise<void> {
  try {
    await confirmBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}

export async function checkInBookingAction(formData: FormData): Promise<void> {
  try {
    await checkInBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}

export async function completeBookingAction(formData: FormData): Promise<void> {
  try {
    await completeBooking(String(formData.get("id") ?? ""), String(formData.get("unused_tokens") ?? "0"));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}

export async function cancelBookingAction(formData: FormData): Promise<void> {
  try {
    await cancelBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}
