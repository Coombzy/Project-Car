"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { createMemberTodo, deleteMemberTodo, patchMemberTodo } from "../../../lib/shop-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "To-do update failed.";
  redirect(`/member?error=${encodeURIComponent(message)}`);
}

function dueFromForm(formData: FormData): string | undefined {
  const raw = String(formData.get("due_at") ?? "").trim();
  return raw || undefined;
}

export async function createMemberTodoAction(formData: FormData): Promise<void> {
  try {
    await createMemberTodo({
      title: String(formData.get("title") ?? "").trim(),
      notes: String(formData.get("notes") ?? "").trim() || undefined,
      due_at: dueFromForm(formData),
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/member");
  redirect("/member");
}

export async function toggleMemberTodoAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  const status = String(formData.get("status") ?? "open") === "done" ? "open" : "done";
  try {
    await patchMemberTodo(id, { status });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/member");
  redirect("/member");
}

export async function deleteMemberTodoAction(formData: FormData): Promise<void> {
  try {
    await deleteMemberTodo(String(formData.get("id") ?? ""));
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/member");
  redirect("/member");
}
