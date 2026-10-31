"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { createHoist, patchHoist } from "../../lib/shop-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Hoist update failed.";
  redirect(`/hoists?error=${encodeURIComponent(message)}`);
}

export async function createHoistAction(formData: FormData): Promise<void> {
  try {
    await createHoist({
      name: String(formData.get("name") ?? "").trim(),
      location_label: String(formData.get("location_label") ?? "").trim(),
      status: String(formData.get("status") ?? "available"),
      is_shop: formData.get("is_shop") === "on",
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/hoists");
  revalidatePath("/");
  revalidatePath("/schedule");
  redirect("/hoists");
}

export async function patchHoistAction(formData: FormData): Promise<void> {
  const status = String(formData.get("status") ?? "available");
  const reason = String(formData.get("reason") ?? "").trim();
  const closing = status === "maintenance" || status === "locked";
  if (closing && (reason.length < 3 || reason.length > 500)) {
    bounce(new ShopApiError(422, "reason_required", "Closing a bay needs a reason."));
  }
  try {
    await patchHoist(String(formData.get("id") ?? ""), {
      location_label: String(formData.get("location_label") ?? "").trim(),
      status,
      is_shop: formData.get("is_shop") === "on",
      ...(closing ? { cancel_bookings: true, reason } : {}),
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/hoists");
  revalidatePath("/");
  revalidatePath("/schedule");
  redirect("/hoists");
}
