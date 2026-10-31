"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { bookingErrorCopy } from "../../../lib/booking-calendar";
import { parseViewParam, scheduleHref } from "../../../lib/calendar";
import { ShopApiError } from "../../../lib/config";
import { snapWholeHourWindow } from "../../../lib/time";
import {
  cancelMemberBooking,
  confirmMemberBooking,
  createMemberBooking,
  quoteMemberBooking,
  requestMemberShopHoist,
} from "../../../lib/shop-api";

function scheduleTarget(formData: FormData): string {
  const view = String(formData.get("view") ?? "");
  const week = String(formData.get("week") ?? "");
  const month = String(formData.get("month") ?? "");
  const hoist = String(formData.get("hoist") ?? "");
  return scheduleHref("/member/schedule", {
    view: parseViewParam(view),
    week: week || undefined,
    month: month || undefined,
    hoist: hoist || undefined,
  });
}

function fail(formData: FormData, error: unknown): never {
  const message = error instanceof ShopApiError ? bookingErrorCopy(error.code, error.message) : "Booking action failed.";
  redirect(scheduleHref("/member/schedule", {
    view: parseViewParam(String(formData.get("view") ?? "")),
    week: String(formData.get("week") ?? "") || undefined,
    month: String(formData.get("month") ?? "") || undefined,
    hoist: String(formData.get("hoist") ?? "") || undefined,
    error: message,
  }));
}

export async function memberCreateBookingAction(formData: FormData): Promise<void> {
  try {
    const window = snapWholeHourWindow(
      String(formData.get("start_at") ?? ""),
      String(formData.get("end_at") ?? ""),
    );
    const quoted = await quoteMemberBooking({
      start_at: window.start,
      end_at: window.end,
    });
    const created = await createMemberBooking({
      hoist_id: String(formData.get("hoist_id") ?? ""),
      start_at: window.start,
      end_at: window.end,
      tokens: quoted.reserved_tokens,
      notes: String(formData.get("notes") ?? "") || null,
    });
    await confirmMemberBooking(created.id);
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(scheduleTarget(formData));
}

export async function memberRequestShopHoistAction(formData: FormData): Promise<void> {
  try {
    const window = snapWholeHourWindow(
      String(formData.get("start_at") ?? ""),
      String(formData.get("end_at") ?? ""),
    );
    await requestMemberShopHoist({
      hoist_id: String(formData.get("hoist_id") ?? ""),
      start_at: window.start,
      end_at: window.end,
      notes: String(formData.get("notes") ?? "") || null,
    });
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(scheduleTarget(formData));
}

export async function memberConfirmBookingAction(formData: FormData): Promise<void> {
  try {
    await confirmMemberBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(scheduleTarget(formData));
}

export async function memberCancelBookingAction(formData: FormData): Promise<void> {
  try {
    if (formData.get("confirm") !== "yes") {
      throw new ShopApiError(400, "confirm_cancel", "Confirm the cancel before it counts.");
    }
    await cancelMemberBooking(String(formData.get("id") ?? ""));
  } catch (error) {
    fail(formData, error);
  }
  revalidatePath("/member/schedule");
  revalidatePath("/member");
  redirect(scheduleTarget(formData));
}
