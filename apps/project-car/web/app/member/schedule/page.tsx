import Link from "next/link";

import { BookingCost } from "../../../components/booking-cost";
import { MemberBookingForm } from "../../../components/member-booking-form";
import { MemberShell } from "../../../components/member-shell";
import { StatusPill } from "../../../components/status-pill";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberFill, getMemberMe, getMemberSchedule } from "../../../lib/shop-api";
import {
  addDays,
  formatShopTime,
  parseWeekParam,
  shopDateTimeLocal,
  shopTodayIso,
  weekdayLabel,
} from "../../../lib/time";
import { memberCancelBookingAction, memberConfirmBookingAction } from "./actions";

export const dynamic = "force-dynamic";

function bookingDay(iso: string): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Edmonton",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(iso));
}

export default async function MemberSchedulePage({
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

    const [me, schedule, fill] = await Promise.all([
      getMemberMe(),
      getMemberSchedule({
        windowStart: `${weekStart}T00:00:00`,
        windowEnd: `${weekEnd}T00:00:00`,
      }),
      getMemberFill(),
    ]);

    return (
      <MemberShell email={me.email} current="schedule" wide>
        <p className="eyebrow">Your week · America/Edmonton</p>
        <h1>Schedule</h1>
        <p className="lede">
          Customer bays only. Reserve is duration × 100 × band × overlay × fill.
          Cancel refunds the locked reserve. The shop hoist is not on this grid.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {fill.applies ? (
          <div className="banner empty">
            Tomorrow ({fill.target_date}, America/Regina) has {fill.open_hours} open
            customer-bay hours. Next-day open slots take a {fill.discount_pct}% fill
            discount (× {fill.fill_multiplier}). Not a public price.
          </div>
        ) : null}

        <div className="week-nav">
          <Link className="button ghost" href={`/member/schedule?week=${addDays(weekStart, -7)}`}>
            ← Previous
          </Link>
          <strong>
            {weekdayLabel(weekStart)} – {weekdayLabel(addDays(weekStart, 6))}
          </strong>
          <Link className="button ghost" href={`/member/schedule?week=${addDays(weekStart, 7)}`}>
            Next →
          </Link>
          <Link className="button ghost" href="/member/schedule">
            This week
          </Link>
        </div>

        {schedule.hoists.length === 0 ? (
          <div className="banner empty">
            No customer bays yet. Ask the Owner to seed demo hoists.
          </div>
        ) : (
          <div className="week-scroll">
            <table className="week-grid">
              <thead>
                <tr>
                  <th>Bay</th>
                  {days.map((day) => (
                    <th key={day} className={day === today ? "is-today" : undefined}>
                      {weekdayLabel(day)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {schedule.hoists.map((hoist) => (
                  <tr key={hoist.id}>
                    <th>
                      <div>{hoist.name}</div>
                      <div className="hoist-pills">
                        <StatusPill value={hoist.status} />
                      </div>
                    </th>
                    {days.map((day) => {
                      const cell = schedule.occupancy.filter(
                        (slot) => slot.hoist_id === hoist.id && bookingDay(slot.start_at) === day,
                      );
                      return (
                        <td key={`${hoist.id}-${day}`} className={day === today ? "is-today" : undefined}>
                          {cell.map((slot) => {
                            const own = slot.own
                              ? schedule.bookings.find((booking) => booking.id === slot.booking_id)
                              : undefined;
                            return (
                              <article
                                key={slot.booking_id}
                                className={`booking-chip status-${slot.status}${slot.own ? "" : " occupancy-chip"}`}
                              >
                                <strong>{slot.own ? "You" : "Booked"}</strong>
                                <div>
                                  {formatShopTime(slot.start_at)}–{formatShopTime(slot.end_at)}
                                </div>
                                {own ? (
                                  <BookingCost
                                    reservedTokens={own.reserved_tokens}
                                    pricingRule={own.pricing_rule}
                                  />
                                ) : null}
                                <StatusPill value={slot.status} />
                                {own && own.status === "pending" ? (
                                  <div className="chip-actions">
                                    <form action={memberConfirmBookingAction}>
                                      <input type="hidden" name="id" value={own.id} />
                                      <input type="hidden" name="week" value={weekStart} />
                                      <button type="submit">Confirm</button>
                                    </form>
                                    <form action={memberCancelBookingAction}>
                                      <input type="hidden" name="id" value={own.id} />
                                      <input type="hidden" name="week" value={weekStart} />
                                      <button className="ghost" type="submit">
                                        Cancel
                                      </button>
                                    </form>
                                  </div>
                                ) : null}
                                {own && (own.status === "confirmed" || own.status === "active") ? (
                                  <div className="chip-actions">
                                    <form action={memberCancelBookingAction}>
                                      <input type="hidden" name="id" value={own.id} />
                                      <input type="hidden" name="week" value={weekStart} />
                                      <button className="ghost" type="submit">
                                        Cancel
                                      </button>
                                    </form>
                                  </div>
                                ) : null}
                              </article>
                            );
                          })}
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
          <h2>Book a customer bay</h2>
          <p className="lede">
            Quote shows band + overlay + fill + total before reserve. Book confirms the
            slot. You cannot book the shop hoist.
          </p>
          {schedule.hoists.length === 0 ? (
            <p className="muted">Need at least one customer bay.</p>
          ) : (
            <MemberBookingForm
              member={me}
              hoists={schedule.hoists}
              weekStart={weekStart}
              defaultStart={shopDateTimeLocal(new Date(Date.now() + 72 * 3600 * 1000))}
              defaultEnd={shopDateTimeLocal(new Date(Date.now() + 73 * 3600 * 1000))}
            />
          )}
        </section>
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="schedule" wide>
        <p className="eyebrow">Your week</p>
        <h1>Schedule</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
