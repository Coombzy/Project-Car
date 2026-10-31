import { BookingCalendar, type CalendarSlot } from "../../../components/booking-calendar";
import { MemberBookingCard } from "../../../components/member-booking-card";
import { MemberShell } from "../../../components/member-shell";
import { MonthHeatmap } from "../../../components/month-heatmap";
import { ScheduleToolbar } from "../../../components/schedule-toolbar";
import { peakWeek } from "../../../lib/booking-calendar";
import { TIME_LABEL } from "../../../lib/booking-words";
import {
  addDays,
  calendarTodayIso,
  monthWindow,
  parseHoistParam,
  parseMonthParam,
  parseViewParam,
  shopWindowQuery,
  sortHoists,
} from "../../../lib/calendar";
import { handleMemberPageError, shopErrorMessage } from "../../../lib/page";
import { getMemberMe, getMemberSchedule, getMemberShopHoist } from "../../../lib/shop-api";
import { parseWeekParam, shopClock } from "../../../lib/time";

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
    const window =
      view === "month" ? monthWindow(month) : { start: weekStart, end: addDays(weekStart, 7) };
    const days = Array.from({ length: 7 }, (_, index) => addDays(weekStart, index));

    let me;
    try {
      me = await getMemberMe();
    } catch (error) {
      const message = await handleMemberPageError(error);
      return (
        <MemberShell current="schedule" wide>
          <p className="eyebrow">Book a bay</p>
          <h1>Book a bay</h1>
          <div className="banner error">{message}</div>
        </MemberShell>
      );
    }

    let loadError: string | null = null;
    const [schedule, shopHoist] = await Promise.all([
      getMemberSchedule({
        windowStart: shopWindowQuery(window.start),
        windowEnd: shopWindowQuery(window.end),
      }).catch((error) => {
        loadError = shopErrorMessage(error, "Could not load your schedule.");
        return { hoists: [], bookings: [], occupancy: [] };
      }),
      getMemberShopHoist().catch(() => null),
    ]);

    const ordered = sortHoists(shopHoist ? [...schedule.hoists, shopHoist] : schedule.hoists);
    const returnTo = { view, week: weekStart, month, hoist: hoistId };
    const peak = peakWeek(
      me.bookings.map((booking) => ({
        status: booking.status,
        startAt: booking.start_at,
        endAt: booking.end_at,
      })),
      weekStart,
    );
    const slots: CalendarSlot[] = schedule.occupancy.map((slot) => ({
      id: slot.booking_id,
      hoistId: slot.hoist_id,
      startAt: slot.start_at,
      endAt: slot.end_at,
      status: slot.status,
      own: slot.own,
      name: slot.own ? "You" : "Booked",
    }));
    const yours = me.bookings.filter(
      (booking) => booking.status === "pending" || booking.status === "confirmed" || booking.status === "no_show",
    );

    return (
      <MemberShell email={me.email} current="schedule" wide>
        <p className="eyebrow">
          Book a bay · {TIME_LABEL}
        </p>
        <h1>Book a bay</h1>
        <p className="lede">
          Balance {me.token_balance} tokens. {peak.line}. Bays 1–5 book on the hour. The shop hoist is ask-first and
          does not hold the hour.
        </p>
        {loadError ? <div className="banner error">{loadError}</div> : null}

        <ScheduleToolbar base="/member/schedule" view={view} weekStart={weekStart} month={month} hoist={hoistId} />

        {ordered.length === 0 ? (
          <div className="banner empty">No bays yet.</div>
        ) : view === "month" ? (
          <MonthHeatmap
            base="/member/schedule"
            month={month}
            hoists={ordered.filter((hoist) => !hoist.is_shop)}
            intervals={schedule.occupancy}
            today={today}
          />
        ) : (
          <BookingCalendar
            view={view}
            days={days}
            today={today}
            nowIso={shopClock().toISOString()}
            hoists={ordered}
            slots={slots}
            balance={me.token_balance}
            returnTo={returnTo}
            error={params.error}
          />
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Your bookings</h2>
          {yours.length === 0 ? (
            <p className="muted">No upcoming bookings. Tap an open hour above.</p>
          ) : (
            yours.map((booking) => {
              const slot = {
                booking_id: booking.id,
                hoist_id: booking.hoist_id,
                hoist_name: booking.hoist_name,
                start_at: booking.start_at,
                end_at: booking.end_at,
                status: booking.status,
                own: true,
              };
              return <MemberBookingCard key={booking.id} slot={slot} own={booking} returnTo={returnTo} />;
            })
          )}
        </section>
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="schedule" wide>
        <p className="eyebrow">Book a bay</p>
        <h1>Book a bay</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
