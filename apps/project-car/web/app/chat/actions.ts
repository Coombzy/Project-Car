"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import type { ChatMessage, ChatMessagePage } from "../../lib/config";
import { ShopApiError } from "../../lib/config";
import { createChatRoom, listChatMessages, muteChatRoom, postChatMessage } from "../../lib/shop-api";

function bounce(path: string, error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Chat update failed.";
  redirect(`${path}${path.includes("?") ? "&" : "?"}error=${encodeURIComponent(message)}`);
}

export async function createRoomAction(formData: FormData): Promise<void> {
  const title = String(formData.get("title") ?? "").trim();
  const memberIds = formData
    .getAll("member_ids")
    .map((value) => String(value).trim())
    .filter(Boolean);
  let room;
  try {
    room = await createChatRoom({ title, member_ids: memberIds });
  } catch (error) {
    bounce("/chat", error);
  }
  revalidatePath("/chat");
  revalidatePath("/member/chat");
  redirect(`/chat/${room.id}`);
}

export async function muteRoomAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  const muted = String(formData.get("muted") ?? "") === "true";
  try {
    await muteChatRoom(id, muted);
  } catch (error) {
    bounce(`/chat/${id}`, error);
  }
  revalidatePath(`/chat/${id}`);
  revalidatePath("/chat");
  redirect(`/chat/${id}`);
}

export async function pollOwnerMessages(roomId: string, afterId?: string): Promise<ChatMessagePage> {
  return listChatMessages(roomId, afterId);
}

export async function sendOwnerMessage(roomId: string, body: string): Promise<ChatMessage> {
  const message = await postChatMessage(roomId, body);
  revalidatePath(`/chat/${roomId}`);
  revalidatePath("/chat");
  return message;
}
