import Link from "next/link";

import { OwnerShell } from "../../components/owner-shell";
import { StatusPill } from "../../components/status-pill";
import { handlePageError } from "../../lib/page";
import { getMe, listBookings, listHoists, listMembers } from "../../lib/shop-api";
import {
  addDays,
  formatShopTime,
  parseWeekParam,
  shopTodayIso,
  weekdayLabel,
} from "../../lib/time";
import {
  cancelBookingAction,
  checkInBookingAction,
  completeBookingAction,
  confirmBookingAction,
  createBookingAction,
} from "./actions";

export const dynamic = "force-dynamic";

function bookingDay(iso: string): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Edmonton",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(iso));
}

export default async function SchedulePage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string; error?: string }>;
}) {
  try {
    const params = await searchParams;
    const weekStart = parseWeekParam(params.week);
    const weekEnd = addDays(weekStart, 7);
    const days = Array.from({ length: 7 }, (_, index) => addDays(weekStart, index));
    const today = shopTodayIso();

    const [me, hoists, members, bookings] = await Promise.all([
      getMe(),
      listHoists(),
      listMembers(),
      listBookings({
        windowStart: `${weekStart}T00:00:00`,
        windowEnd: `${weekEnd}T00:00:00`,
      }),
    ]);

    const activeMembers = members.filter((member) => member.status === "active");

    return (
      <OwnerShell email={me.email} current="schedule" wide>
        <p className="eyebrow">Week view · America/Edmonton</p>
        <h1>Schedule</h1>
        <p className="lede">
          One hoist, one overlapping confirmed or active booking. Create reserves
          tokens; complete debits; cancel refunds.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}

        <div className="week-nav">
          <Link className="button ghost" href={`/schedule?week=${addDays(weekStart, -7)}`}>
            ← Previous
          </Link>
          <strong>
            {weekdayLabel(weekStart)} – {weekdayLabel(addDays(weekStart, 6))}
          </strong>
          <Link className="button ghost" href={`/schedule?week=${addDays(weekStart, 7)}`}>
            Next →
          </Link>
          <Link className="button ghost" href="/schedule">
            This week
          </Link>
        </div>

        {hoists.length === 0 ? (
          <div className="banner empty">
            Seed demo hoists with <code>python -m app.seed</code> or add one on{" "}
            <Link href="/hoists">Hoists</Link>.
          </div>
        ) : (
          <div className="week-scroll">
            <table className="week-grid">
              <thead>
                <tr>
                  <th>Hoist</th>
                  {days.map((day) => (
                    <th key={day} className={day === today ? "is-today" : undefined}>
                      {weekdayLabel(day)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {hoists.map((hoist) => (
                  <tr key={hoist.id}>
                    <th>
                      <div>{hoist.name}</div>
                      <StatusPill value={hoist.status} />
                    </th>
                    {days.map((day) => {
                      const cell = bookings.filter(
                        (booking) =>
                          booking.hoist_id === hoist.id && bookingDay(booking.start_at) === day,
                      );
                      return (
                        <td key={`${hoist.id}-${day}`} className={day === today ? "is-today" : undefined}>
                          {cell.map((booking) => (
                            <article key={booking.id} className={`booking-chip status-${booking.status}`}>
                              <strong>{booking.member_name}</strong>
                              <div>
                                {formatShopTime(booking.start_at)}–{formatShopTime(booking.end_at)}
                              </div>
                              <StatusPill value={booking.status} />
                              <div className="chip-actions">
                                {booking.status === "pending" ? (
                                  <form action={confirmBookingAction}>
                                    <input type="hidden" name="id" value={booking.id} />
                                    <input type="hidden" name="week" value={weekStart} />
                                    <button type="submit">Confirm</button>
                                  </form>
                                ) : null}
                                {booking.status === "confirmed" ? (
                                  <form action={checkInBookingAction}>
                                    <input type="hidden" name="id" value={booking.id} />
                                    <input type="hidden" name="week" value={weekStart} />
                                    <button type="submit">Check in</button>
                                  </form>
                                ) : null}
                                {booking.status === "active" ? (
                                  <form action={completeBookingAction}>
                                    <input type="hidden" name="id" value={booking.id} />
                                    <input type="hidden" name="week" value={weekStart} />
                                    <input type="hidden" name="unused_tokens" value="0" />
                                    <button type="submit">Complete</button>
                                  </form>
                                ) : null}
                                {booking.status === "pending" ||
                                booking.status === "confirmed" ||
                                booking.status === "active" ? (
                                  <form action={cancelBookingAction}>
                                    <input type="hidden" name="id" value={booking.id} />
                                    <input type="hidden" name="week" value={weekStart} />
                                    <button className="ghost" type="submit">
                                      Cancel
                                    </button>
                                  </form>
                                ) : null}
                              </div>
                            </article>
                          ))}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Create booking</h2>
          <p className="lede">
            Starts as pending and reserves tokens. Confirm to hold the bay.
          </p>
          {activeMembers.length === 0 || hoists.length === 0 ? (
            <p className="muted">Need at least one active member and one hoist.</p>
          ) : (
            <form action={createBookingAction} className="stack-form">
              <input type="hidden" name="week" value={weekStart} />
              <div className="form-grid">
                <label>
                  Member
                  <select name="member_id" required defaultValue={activeMembers[0]?.id}>
                    {activeMembers.map((member) => (
                      <option key={member.id} value={member.id}>
                        {member.name} · {member.tier_name} · {member.token_balance} tok
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Hoist
                  <select name="hoist_id" required defaultValue={hoists[0]?.id}>
                    {hoists.map((hoist) => (
                      <option key={hoist.id} value={hoist.id}>
                        {hoist.name} · {hoist.status}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Start
                  <input type="datetime-local" name="start_at" required />
                </label>
                <label>
                  End
                  <input type="datetime-local" name="end_at" required />
                </label>
                <label>
                  Tokens to reserve
                  <input type="number" name="tokens" min="1" step="1" defaultValue="1" />
                </label>
                <label>
                  Notes
                  <input type="text" name="notes" placeholder="Optional" />
                </label>
              </div>
              <div className="actions">
                <button type="submit">Reserve booking</button>
              </div>
            </form>
          )}
        </section>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="schedule" wide>
        <p className="eyebrow">Week view</p>
        <h1>Schedule</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
