"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { adjustMemberTokens, createMember, patchMember } from "../../lib/shop-api";

function bounce(path: string, error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Member update failed.";
  redirect(`${path}${path.includes("?") ? "&" : "?"}error=${encodeURIComponent(message)}`);
}

export async function createMemberAction(formData: FormData): Promise<void> {
  try {
    await createMember({
      name: String(formData.get("name") ?? "").trim(),
      email: String(formData.get("email") ?? "").trim(),
      phone: String(formData.get("phone") ?? "").trim() || null,
      tier_name: String(formData.get("tier_name") ?? "basic"),
      status: String(formData.get("status") ?? "active"),
    });
  } catch (error) {
    bounce("/members", error);
  }
  revalidatePath("/members");
  revalidatePath("/");
  redirect("/members");
}

export async function patchMemberAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  try {
    await patchMember(id, {
      name: String(formData.get("name") ?? "").trim(),
      phone: String(formData.get("phone") ?? "").trim() || null,
      tier_name: String(formData.get("tier_name") ?? ""),
      status: String(formData.get("status") ?? "active"),
      waiver_version: String(formData.get("waiver_version") ?? "").trim() || null,
      emergency_contact_name: String(formData.get("emergency_contact_name") ?? "").trim() || null,
      emergency_contact_phone: String(formData.get("emergency_contact_phone") ?? "").trim() || null,
    });
  } catch (error) {
    bounce(`/members/${id}`, error);
  }
  revalidatePath(`/members/${id}`);
  revalidatePath("/members");
  redirect(`/members/${id}`);
}

export async function adjustTokensAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  try {
    await adjustMemberTokens(
      id,
      String(formData.get("amount") ?? ""),
      String(formData.get("note") ?? "Owner adjustment"),
    );
  } catch (error) {
    bounce(`/members/${id}`, error);
  }
  revalidatePath(`/members/${id}`);
  revalidatePath("/");
  redirect(`/members/${id}`);
}
