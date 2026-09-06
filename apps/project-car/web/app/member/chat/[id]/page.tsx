import Link from "next/link";

import { ChatThread } from "../../../../components/chat-thread";
import { MemberShell } from "../../../../components/member-shell";
import { handleMemberPageError } from "../../../../lib/page";
import { getMemberChatRoom, getMemberMe, listMemberChatMessages } from "../../../../lib/shop-api";
import { pollMemberMessages, sendMemberMessage } from "../actions";

export const dynamic = "force-dynamic";

export default async function MemberChatRoomPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  try {
    const { id } = await params;
    const [me, room, page] = await Promise.all([
      getMemberMe(),
      getMemberChatRoom(id),
      listMemberChatMessages(id),
    ]);
    return (
      <MemberShell email={me.email} current="chat">
        <p className="eyebrow">
          <Link href="/member/chat">Your rooms</Link>
          {" · "}
          GET /member/chat/rooms/{id}
        </p>
        <h1>{room.title}</h1>
        <p className="lede">
          Reply in this Owner-started room. Polls every few seconds while open.
        </p>
        <div className="banner demo">
          Not live Matrix / demo. Human shop chat. You cannot start rooms.
        </div>
        <ChatThread
          room={room}
          initialMessages={page.messages}
          initialCursor={page.cursor}
          pollMessages={pollMemberMessages}
          sendMessage={sendMemberMessage}
        />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="chat">
        <p className="eyebrow">
          <Link href="/member/chat">Your rooms</Link>
        </p>
        <h1>Shop chat</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
