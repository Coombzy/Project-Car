import Link from "next/link";

import { CreateBookingForm } from "../../components/create-booking-form";
import { MonthHeatmap } from "../../components/month-heatmap";
import { OwnerBookingCard } from "../../components/owner-booking-card";
import { OwnerShell } from "../../components/owner-shell";
import { ScheduleToolbar } from "../../components/schedule-toolbar";
import { WeekHoistCalendars } from "../../components/week-hoist-calendars";
import { handlePageError, shopErrorMessage } from "../../lib/page";
import { getMe, listBookings, listHoists, listMembers } from "../../lib/shop-api";
import {
  addDays,
  calendarTodayIso,
  monthWindow,
  parseHoistParam,
  parseMonthParam,
  parseSlotParam,
  parseViewParam,
  shopWindowQuery,
  slotEnd,
  sortHoists,
} from "../../lib/calendar";
import { parseWeekParam, shopDateTimeLocal } from "../../lib/time";

export const dynamic = "force-dynamic";

export default async function SchedulePage({
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

    let me;
    try {
      me = await getMe();
    } catch (error) {
      const message = await handlePageError(error);
      return (
        <OwnerShell current="schedule" wide>
          <p className="eyebrow">Schedule</p>
          <h1>Schedule</h1>
          <div className="banner error">{message}</div>
        </OwnerShell>
      );
    }

    let loadError: string | null = null;
    const [hoists, members, bookings] = await Promise.all([
      listHoists().catch((error) => {
        loadError = shopErrorMessage(error, "Could not load hoists.");
        return [];
      }),
      listMembers().catch((error) => {
        loadError = shopErrorMessage(error, "Could not load members.");
        return [];
      }),
      listBookings({
        windowStart: shopWindowQuery(window.start),
        windowEnd: shopWindowQuery(window.end),
      }).catch((error) => {
        loadError = shopErrorMessage(error, "Could not load bookings.");
        return [];
      }),
    ]);

    const ordered = sortHoists(hoists);
    const activeMembers = members.filter((member) => member.status === "active");
    const returnTo = { view, week: weekStart, month, hoist: hoistId };
    const defaultStart = slot ?? shopDateTimeLocal(new Date(Date.now() + 72 * 3600 * 1000));
    const defaultEnd = slot ? slotEnd(slot) : shopDateTimeLocal(new Date(Date.now() + 73 * 3600 * 1000));

    return (
      <OwnerShell email={me.email} current="schedule" wide>
        <p className="eyebrow">
          {view === "month" ? "Month heat-map" : "Week · per hoist"} · America/Regina
        </p>
        <h1>Schedule</h1>
        <p className="lede">
          Management calendar on ops.projectcar.ca (LIVE when Doc is up;
          app. is the temporary alias). Month shows how booked each hoist is that day
          (Bays 1–5 plus the Owner-only shop hoist). Week is a separate hour
          grid per hoist. Reserve is duration × 100 × band × overlay × fill.
          Complete debits; cancel refunds the locked reserve.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {loadError ? <div className="banner error">{loadError}</div> : null}

        <ScheduleToolbar base="/schedule" view={view} weekStart={weekStart} month={month} hoist={hoistId} />

        {ordered.length === 0 ? (
          <div className="banner empty">
            Seed demo hoists with <code>python -m app.seed</code> or add one on{" "}
            <Link href="/hoists">Hoists</Link>.
          </div>
        ) : view === "month" ? (
          <MonthHeatmap
            base="/schedule"
            month={month}
            hoists={ordered}
            intervals={bookings}
            today={today}
          />
        ) : (
          <WeekHoistCalendars
            base="/schedule"
            weekStart={weekStart}
            month={month}
            days={days}
            today={today}
            hoists={ordered}
            focusHoistId={hoistId}
            itemsForHoist={(hoist) =>
              bookings
                .filter((booking) => booking.hoist_id === hoist.id)
                .map((booking) => ({
                  id: booking.id,
                  start_at: booking.start_at,
                  end_at: booking.end_at,
                  node: <OwnerBookingCard booking={booking} returnTo={returnTo} compact />,
                }))
            }
          />
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Create booking</h2>
          <p className="lede">
            Customer bookings start pending; the server computes reserve from the
            window. Shop work is Owner-only on the shop hoist (customers cannot
            book it) and does not take member tokens.
            {slot ? ` Prefilling ${slot} from the hour slot you clicked.` : ""}
          </p>
          {activeMembers.length === 0 || ordered.length === 0 ? (
            <p className="muted">Need at least one active member and one hoist.</p>
          ) : (
            <CreateBookingForm
              key={`${defaultStart}-${hoistId ?? ""}`}
              members={activeMembers}
              hoists={ordered}
              weekStart={weekStart}
              defaultStart={defaultStart}
              defaultEnd={defaultEnd}
              defaultHoistId={hoistId}
              returnTo={returnTo}
            />
          )}
        </section>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="schedule" wide>
        <p className="eyebrow">Schedule</p>
        <h1>Schedule</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
