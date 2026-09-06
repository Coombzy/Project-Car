import Link from "next/link";

import { ChatThread } from "../../../components/chat-thread";
import { OwnerShell } from "../../../components/owner-shell";
import { handlePageError } from "../../../lib/page";
import { getChatRoom, getMe, listChatMessages } from "../../../lib/shop-api";
import { muteRoomAction, pollOwnerMessages, sendOwnerMessage } from "../actions";

export const dynamic = "force-dynamic";

export default async function OwnerChatRoomPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const [{ id }, query] = await Promise.all([params, searchParams]);
    const [me, room, page] = await Promise.all([getMe(), getChatRoom(id), listChatMessages(id)]);
    return (
      <OwnerShell email={me.email} current="chat">
        <p className="eyebrow">
          <Link href="/chat">All rooms</Link>
          {" · "}
          GET /chat/rooms/{id}
        </p>
        <div className="hoist-card-head">
          <h1>{room.title}</h1>
          {room.muted ? <span className="pill">Muted</span> : null}
        </div>
        <p className="lede">
          {room.participants.map((row) => row.name).join(", ") || "No members"} · polling
          every few seconds. Human messages only.
        </p>
        <div className="banner demo">
          Not live Matrix / demo. Owner/ops can mute this thread. Members cannot
          start rooms.
        </div>
        {query.error ? <div className="banner error">{query.error}</div> : null}
        <form action={muteRoomAction} className="chat-mute">
          <input type="hidden" name="id" value={room.id} />
          <input type="hidden" name="muted" value={room.muted ? "false" : "true"} />
          <button className="ghost" type="submit">
            {room.muted ? "Unmute thread" : "Mute thread"}
          </button>
        </form>
        <ChatThread
          room={room}
          initialMessages={page.messages}
          initialCursor={page.cursor}
          pollMessages={pollOwnerMessages}
          sendMessage={sendOwnerMessage}
        />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="chat">
        <p className="eyebrow">
          <Link href="/chat">All rooms</Link>
        </p>
        <h1>Shop chat</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
