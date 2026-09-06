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
  try {
    await patchHoist(String(formData.get("id") ?? ""), {
      location_label: String(formData.get("location_label") ?? "").trim(),
      status: String(formData.get("status") ?? "available"),
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/hoists");
  revalidatePath("/");
  revalidatePath("/schedule");
  redirect("/hoists");
}
