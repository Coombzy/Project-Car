import Link from "next/link";

import { BookingCost } from "../../components/booking-cost";
import { CreateBookingForm } from "../../components/create-booking-form";
import { OwnerShell } from "../../components/owner-shell";
import { StatusPill } from "../../components/status-pill";
import { handlePageError } from "../../lib/page";
import { getMe, listBookings, listHoists, listMembers } from "../../lib/shop-api";
import {
  addDays,
  formatShopTime,
  parseWeekParam,
  shopDateTimeLocal,
  shopTodayIso,
  weekdayLabel,
} from "../../lib/time";
import {
  cancelBookingAction,
  checkInBookingAction,
  completeBookingAction,
  confirmBookingAction,
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
          Six bays — the shop hoist is reserved for internal work first.
          Customer bookings cannot displace open shop work. Reserve cost is
          duration × 100 × band × overlay. Complete debits; cancel refunds the
          locked reserve.
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
                      <div className="hoist-pills">
                        {hoist.is_shop ? <StatusPill value="shop" /> : null}
                        <StatusPill value={hoist.status} />
                      </div>
                    </th>
                    {days.map((day) => {
                      const cell = bookings.filter(
                        (booking) =>
                          booking.hoist_id === hoist.id && bookingDay(booking.start_at) === day,
                      );
                      return (
                        <td key={`${hoist.id}-${day}`} className={day === today ? "is-today" : undefined}>
                          {cell.map((booking) => (
                            <article key={booking.id} className={`booking-chip status-${booking.status}${booking.kind === "shop" ? " booking-chip-shop" : ""}`}>
                              <strong>{booking.member_name}</strong>
                              {booking.kind === "shop" ? <StatusPill value="shop" /> : null}
                              <div>
                                {formatShopTime(booking.start_at)}–{formatShopTime(booking.end_at)}
                              </div>
                              <BookingCost
                                reservedTokens={booking.reserved_tokens}
                                pricingRule={booking.pricing_rule}
                              />
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
            Customer bookings start pending; the server computes reserve from the
            window. Shop work is Owner-only on the shop hoist and does not take
            member tokens.
          </p>
          {activeMembers.length === 0 || hoists.length === 0 ? (
            <p className="muted">Need at least one active member and one hoist.</p>
          ) : (
            <CreateBookingForm
              members={activeMembers}
              hoists={hoists}
              weekStart={weekStart}
              defaultStart={shopDateTimeLocal(new Date(Date.now() + 72 * 3600 * 1000))}
              defaultEnd={shopDateTimeLocal(new Date(Date.now() + 73 * 3600 * 1000))}
            />
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
