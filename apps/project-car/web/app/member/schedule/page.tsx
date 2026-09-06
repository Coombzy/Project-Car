import { MemberBookingCard } from "../../../components/member-booking-card";
import { MemberBookingForm } from "../../../components/member-booking-form";
import { MemberShell } from "../../../components/member-shell";
import { MonthHeatmap } from "../../../components/month-heatmap";
import { ScheduleToolbar } from "../../../components/schedule-toolbar";
import { WeekHoistCalendars } from "../../../components/week-hoist-calendars";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberFill, getMemberMe, getMemberSchedule } from "../../../lib/shop-api";
import {
  addDays,
  calendarTodayIso,
  monthWindow,
  naiveWindow,
  parseHoistParam,
  parseMonthParam,
  parseSlotParam,
  parseViewParam,
  slotEnd,
  sortHoists,
} from "../../../lib/calendar";
import { parseWeekParam, shopDateTimeLocal } from "../../../lib/time";

export const dynamic = "force-dynamic";

export default async function MemberSchedulePage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string; month?: string; view?: string; hoist?: string; slot?: string; error?: string }>;
}) {
  try {
    const params = await searchParams;
    const today = calendarTodayIso();
    const view = parseViewParam(params.view, params.week);
    const weekStart = parseWeekParam(params.week);
    const month = parseMonthParam(params.month, params.week ? weekStart : today);
    const hoistId = parseHoistParam(params.hoist);
    const slot = parseSlotParam(params.slot);
    const window =
      view === "month"
        ? monthWindow(month)
        : { start: weekStart, end: addDays(weekStart, 7) };
    const days = Array.from({ length: 7 }, (_, index) => addDays(weekStart, index));

    const [me, schedule, fill] = await Promise.all([
      getMemberMe(),
      getMemberSchedule({
        windowStart: naiveWindow(window.start),
        windowEnd: naiveWindow(window.end),
      }),
      getMemberFill().catch(() => null),
    ]);

    const ordered = sortHoists(schedule.hoists.filter((hoist) => !hoist.is_shop));
    const returnTo = { view, week: weekStart, month, hoist: hoistId };
    const defaultStart = slot ?? shopDateTimeLocal(new Date(Date.now() + 72 * 3600 * 1000));
    const defaultEnd = slot ? slotEnd(slot) : shopDateTimeLocal(new Date(Date.now() + 73 * 3600 * 1000));

    return (
      <MemberShell email={me.email} current="schedule" wide>
        <p className="eyebrow">
          {view === "month" ? "Month heat-map" : "Week · per bay"} · America/Regina
        </p>
        <h1>Schedule</h1>
        <p className="lede">
          Customer bays only. Month is a density heat-map; week is an hour grid
          per bay. Reserve is duration × 100 × band × overlay × fill. Cancel
          refunds the locked reserve. The shop hoist is not on this calendar.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {fill?.applies ? (
          <div className="banner empty">
            Tomorrow ({fill.target_date}, America/Regina) has {fill.open_hours} open
            customer-bay hours. Next-day open slots take a {fill.discount_pct}% fill
            discount (× {fill.fill_multiplier}). Not a public price.
          </div>
        ) : null}

        <ScheduleToolbar
          base="/member/schedule"
          view={view}
          weekStart={weekStart}
          month={month}
          hoist={hoistId}
        />

        {ordered.length === 0 ? (
          <div className="banner empty">No customer bays yet. Ask the Owner to seed demo hoists.</div>
        ) : view === "month" ? (
          <MonthHeatmap
            base="/member/schedule"
            month={month}
            hoists={ordered}
            intervals={schedule.occupancy}
            today={today}
          />
        ) : (
          <WeekHoistCalendars
            base="/member/schedule"
            weekStart={weekStart}
            month={month}
            days={days}
            today={today}
            hoists={ordered}
            focusHoistId={hoistId}
            itemsForHoist={(hoist) =>
              schedule.occupancy
                .filter((slotRow) => slotRow.hoist_id === hoist.id)
                .map((slotRow) => {
                  const own = slotRow.own
                    ? schedule.bookings.find((booking) => booking.id === slotRow.booking_id)
                    : undefined;
                  return {
                    id: slotRow.booking_id,
                    start_at: slotRow.start_at,
                    end_at: slotRow.end_at,
                    node: <MemberBookingCard slot={slotRow} own={own} returnTo={returnTo} compact />,
                  };
                })
            }
          />
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Book a customer bay</h2>
          <p className="lede">
            Quote shows band + overlay + fill + total before reserve. Book confirms the
            slot. You cannot book the shop hoist.
            {slot ? ` Prefilling ${slot} from the hour slot you clicked.` : ""}
          </p>
          {ordered.length === 0 ? (
            <p className="muted">Need at least one customer bay.</p>
          ) : (
            <MemberBookingForm
              key={`${defaultStart}-${hoistId ?? ""}`}
              member={me}
              hoists={ordered}
              weekStart={weekStart}
              defaultStart={defaultStart}
              defaultEnd={defaultEnd}
              defaultHoistId={hoistId}
              returnTo={returnTo}
            />
          )}
        </section>
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="schedule" wide>
        <p className="eyebrow">Your schedule</p>
        <h1>Schedule</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
