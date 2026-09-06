import Link from "next/link";

import { MemberShell } from "../../../components/member-shell";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe, listMemberChatRooms } from "../../../lib/shop-api";
import { formatShopDateTime } from "../../../lib/time";

export const dynamic = "force-dynamic";

export default async function MemberChatPage() {
  try {
    const [me, rooms] = await Promise.all([getMemberMe(), listMemberChatRooms()]);
    return (
      <MemberShell email={me.email} current="chat">
        <p className="eyebrow">GET /member/chat/rooms · your rooms only</p>
        <h1>Shop chat</h1>
        <p className="lede">
          Owner starts rooms. You can reply in threads you are in. Polling demo —
          not live Matrix, not Apex, not Grok.
        </p>
        <div className="banner demo">
          Not live Matrix / demo. Human messages only. You cannot create a room
          from Member. The shop is not open.
        </div>
        {rooms.length === 0 ? (
          <div className="banner empty">No rooms yet. Owner has not started a thread with you.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>Room</th>
                  <th>Last message</th>
                </tr>
              </thead>
              <tbody>
                {rooms.map((room) => (
                  <tr key={room.id}>
                    <td>
                      <Link href={`/member/chat/${room.id}`}>{room.title}</Link>
                    </td>
                    <td className="notes">
                      {room.last_message
                        ? `${room.last_message.sender_name}: ${room.last_message.body}`
                        : "No messages"}
                      {room.last_message_at ? (
                        <div className="muted">{formatShopDateTime(room.last_message_at)}</div>
                      ) : null}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="chat">
        <p className="eyebrow">Shop chat</p>
        <h1>Shop chat</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
