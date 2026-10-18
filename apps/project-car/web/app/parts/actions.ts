"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError, type PartsOrder } from "../../lib/config";
import { patchPartsOrder, patchPartsRequest } from "../../lib/shop-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Parts update failed.";
  redirect(`/parts?error=${encodeURIComponent(message)}`);
}

function orderStatus(value: string): PartsOrder["status"] | null {
  switch (value) {
    case "ordered":
    case "shipped":
    case "in_transit":
    case "received":
      return value;
    default:
      return null;
  }
}

function requestDecision(value: string): "fulfilled" | "declined" | null {
  switch (value) {
    case "fulfilled":
    case "declined":
      return value;
    default:
      return null;
  }
}

export async function patchPartsOrderAction(formData: FormData): Promise<void> {
  const status = orderStatus(String(formData.get("status") ?? ""));
  if (!status) {
    redirect(`/parts?error=${encodeURIComponent("Choose ordered, shipped, in transit, or received.")}`);
  }
  try {
    await patchPartsOrder(String(formData.get("id") ?? ""), status);
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/parts");
  revalidatePath("/");
  redirect("/parts");
}

export async function decidePartsRequestAction(formData: FormData): Promise<void> {
  const status = requestDecision(String(formData.get("status") ?? ""));
  if (!status) {
    redirect(`/parts?error=${encodeURIComponent("Choose fulfilled or declined.")}`);
  }
  try {
    await patchPartsRequest(String(formData.get("id") ?? ""), status);
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/parts");
  revalidatePath("/member/parts");
  redirect("/parts");
}
