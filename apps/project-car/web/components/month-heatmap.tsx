import Link from "next/link";

import {
  hoistChipLabel,
  hoistDayDensity,
  mondayOf,
  monthGrid,
  scheduleHref,
  type CalendarInterval,
} from "../lib/calendar";
import type { Hoist } from "../lib/config";
import { weekdayLabel } from "../lib/time";

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export function MonthHeatmap({
  base,
  month,
  hoists,
  intervals,
  today,
}: {
  base: "/schedule" | "/member/schedule";
  month: string;
  hoists: Hoist[];
  intervals: CalendarInterval[];
  today: string;
}) {
  const weeks = monthGrid(month);

  return (
    <div className="month-wrap">
      <div className="density-legend" aria-label="Booking density">
        <span className="muted">Density vs 08:00–21:00</span>
        {(["empty", "light", "medium", "heavy", "full"] as const).map((level) => (
          <span key={level} className={`density-swatch density-${level}`}>
            {level}
          </span>
        ))}
      </div>
      <div className="month-grid">
        {WEEKDAYS.map((label) => (
          <div key={label} className="month-dow">
            {label}
          </div>
        ))}
        {weeks.flatMap((week) =>
          week.map((day) => {
            const inMonth = day.startsWith(month);
            const weekStart = mondayOf(day);
            return (
              <div
                key={day}
                className={`month-day${day === today ? " is-today" : ""}${inMonth ? "" : " is-outside"}`}
              >
                <Link
                  className="month-day-link"
                  href={scheduleHref(base, { view: "week", week: weekStart, month, hoist: hoists[0]?.id })}
                >
                  <span className="month-day-num">{Number(day.slice(8))}</span>
                  <span className="sr-only">{weekdayLabel(day)} — open week</span>
                </Link>
                <div className="month-chips">
                  {hoists.map((hoist) => {
                    const density = hoistDayDensity(intervals, hoist.id, day);
                    const title = [
                      hoist.name,
                      hoist.is_shop ? "Owner-only" : null,
                      `${density.bookedHours.toFixed(density.bookedHours % 1 ? 2 : 0)}h booked`,
                      density.level,
                    ]
                      .filter(Boolean)
                      .join(" · ");
                    return (
                      <Link
                        key={hoist.id}
                        href={scheduleHref(base, { view: "week", week: weekStart, month, hoist: hoist.id })}
                        className={`density-chip density-${density.level}${hoist.is_shop ? " density-chip-shop" : ""}`}
                        title={title}
                      >
                        <span>{hoistChipLabel(hoist.name, hoist.is_shop)}</span>
                        {hoist.is_shop ? <em>Owner</em> : null}
                      </Link>
                    );
                  })}
                </div>
              </div>
            );
          }),
        )}
      </div>
    </div>
  );
}
