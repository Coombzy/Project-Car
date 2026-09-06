import Link from "next/link";

import {
  addDays,
  addMonths,
  formatMonthLabel,
  scheduleHref,
  type ScheduleView,
} from "../lib/calendar";
import { weekdayLabel } from "../lib/time";

export function ScheduleToolbar({
  base,
  view,
  weekStart,
  month,
  hoist,
}: {
  base: "/schedule" | "/member/schedule";
  view: ScheduleView;
  weekStart: string;
  month: string;
  hoist?: string;
}) {
  const weekHref = (week: string) => scheduleHref(base, { view: "week", week, month, hoist });
  const monthHref = (nextMonth: string) => scheduleHref(base, { view: "month", month: nextMonth, week: weekStart });

  return (
    <div className="schedule-toolbar">
      <div className="view-toggle" role="tablist" aria-label="Schedule view">
        <Link
          className={`button ghost${view === "month" ? " is-active" : ""}`}
          href={monthHref(month)}
          aria-current={view === "month" ? "page" : undefined}
        >
          Month
        </Link>
        <Link
          className={`button ghost${view === "week" ? " is-active" : ""}`}
          href={weekHref(weekStart)}
          aria-current={view === "week" ? "page" : undefined}
        >
          Week
        </Link>
      </div>
      <div className="week-nav">
        {view === "month" ? (
          <>
            <Link className="button ghost" href={monthHref(addMonths(month, -1))}>
              ← Previous
            </Link>
            <strong>{formatMonthLabel(month)}</strong>
            <Link className="button ghost" href={monthHref(addMonths(month, 1))}>
              Next →
            </Link>
            <Link className="button ghost" href={scheduleHref(base, { view: "month" })}>
              This month
            </Link>
          </>
        ) : (
          <>
            <Link className="button ghost" href={weekHref(addDays(weekStart, -7))}>
              ← Previous
            </Link>
            <strong>
              {weekdayLabel(weekStart)} – {weekdayLabel(addDays(weekStart, 6))}
            </strong>
            <Link className="button ghost" href={weekHref(addDays(weekStart, 7))}>
              Next →
            </Link>
            <Link className="button ghost" href={scheduleHref(base, { view: "week", month })}>
              This week
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
