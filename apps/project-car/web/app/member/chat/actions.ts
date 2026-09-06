"use server";

import type { ChatMessage, ChatMessagePage } from "../../../lib/config";
import { listMemberChatMessages, postMemberChatMessage } from "../../../lib/shop-api";
import { revalidatePath } from "next/cache";

export async function pollMemberMessages(roomId: string, afterId?: string): Promise<ChatMessagePage> {
  return listMemberChatMessages(roomId, afterId);
}

export async function sendMemberMessage(roomId: string, body: string): Promise<ChatMessage> {
  const message = await postMemberChatMessage(roomId, body);
  revalidatePath(`/member/chat/${roomId}`);
  revalidatePath("/member/chat");
  return message;
}
