import Link from "next/link";

import { OwnerShell } from "../../components/owner-shell";
import { handlePageError } from "../../lib/page";
import { getMe, listChatRooms, listMembers } from "../../lib/shop-api";
import { formatShopDateTime } from "../../lib/time";
import { createRoomAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function OwnerChatPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, rooms, members] = await Promise.all([getMe(), listChatRooms(), listMembers()]);
    const activeMembers = members.filter((member) => member.status === "active");
    return (
      <OwnerShell email={me.email} current="chat">
        <p className="eyebrow">GET /chat/rooms · Owner starts rooms</p>
        <h1>Shop chat</h1>
        <p className="lede">
          Human messaging only. Owner starts a room and picks member(s). Ops/Owner
          see every thread and can mute. Members reply from <code>/member/chat</code>.
          Polling demo — not live Matrix, not Apex, not Grok.
        </p>
        <div className="banner demo">
          Not live Matrix / demo. Human shop chat with a few-second poll while a
          thread is open. The shop is not open.
        </div>
        {params.error ? <div className="banner error">{params.error}</div> : null}

        {rooms.length === 0 ? (
          <div className="banner empty">No rooms yet. Create one below, or seed the demo.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>Room</th>
                  <th>Members</th>
                  <th>Last message</th>
                  <th>Mute</th>
                </tr>
              </thead>
              <tbody>
                {rooms.map((room) => (
                  <tr key={room.id}>
                    <td>
                      <Link href={`/chat/${room.id}`}>{room.title}</Link>
                    </td>
                    <td>{room.participants.map((row) => row.name).join(", ") || "—"}</td>
                    <td className="notes">
                      {room.last_message
                        ? `${room.last_message.sender_name}: ${room.last_message.body}`
                        : "No messages"}
                      {room.last_message_at ? (
                        <div className="muted">{formatShopDateTime(room.last_message_at)}</div>
                      ) : null}
                    </td>
                    <td>{room.muted ? "Muted" : "Open"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Start a room</h2>
          <p className="lede">Owner only. Pick one or more members who can reply.</p>
          <form action={createRoomAction} className="stack-form">
            <label>
              Title
              <input name="title" required maxLength={200} placeholder="Ada — turbo mock-up" />
            </label>
            <fieldset className="chat-member-picker">
              <legend>Members</legend>
              {activeMembers.length === 0 ? (
                <p className="muted">No active members to add.</p>
              ) : (
                activeMembers.map((member) => (
                  <label key={member.id} className="checkbox-row">
                    <input type="checkbox" name="member_ids" value={member.id} />
                    {member.name}
                    <span className="muted">{member.email}</span>
                  </label>
                ))
              )}
            </fieldset>
            <div className="actions">
              <button type="submit" disabled={activeMembers.length === 0}>
                Create room
              </button>
            </div>
          </form>
        </section>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="chat">
        <p className="eyebrow">Shop chat</p>
        <h1>Shop chat</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
