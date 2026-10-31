"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { parseViewParam, scheduleHref } from "../../lib/calendar";
import { snapWholeHourWindow } from "../../lib/time";
import { ShopApiError } from "../../lib/config";
import {
  approveShopHoistRequest,
  cancelBooking,
  checkInBooking,
  completeBooking,
  confirmBooking,
  createBooking,
  denyShopHoistRequest,
} from "../../lib/shop-api";

function scheduleTarget(formData: FormData): string {
  const view = String(formData.get("view") ?? "");
  const week = String(formData.get("week") ?? "");
  const month = String(formData.get("month") ?? "");
  const hoist = String(formData.get("hoist") ?? "");
  return scheduleHref("/schedule", {
    view: parseViewParam(view),
    week: week || undefined,
    month: month || undefined,
    hoist: hoist || undefined,
  });
}

function fail(formData: FormData, error: unknown, fallback = "Booking action failed."): never {
  const message = error instanceof ShopApiError ? error.message : fallback;
  redirect(scheduleHref("/schedule", {
    view: parseViewParam(String(formData.get("view") ?? "")),
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
    const window = snapWholeHourWindow(
      String(formData.get("start_at") ?? ""),
      String(formData.get("end_at") ?? ""),
    );
    await createBooking({
      member_id: kind === "shop" ? memberId || null : memberId,
      hoist_id: String(formData.get("hoist_id") ?? ""),
      start_at: window.start,
      end_at: window.end,
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
    await completeBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}

export async function approveShopHoistRequestAction(formData: FormData): Promise<void> {
  try {
    await approveShopHoistRequest(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error, "Could not approve the shop hoist request.");
  }
  revalidatePath("/schedule");
  revalidatePath("/");
  redirect(scheduleTarget(formData));
}

export async function denyShopHoistRequestAction(formData: FormData): Promise<void> {
  try {
    await denyShopHoistRequest(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error, "Could not deny the shop hoist request.");
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
