import type { ReactNode } from "react";
import Link from "next/link";

import {
  OPEN_HOUR_END,
  OPEN_HOUR_START,
  bookingHourPlacement,
  hoistChipLabel,
  hourLabels,
  scheduleHref,
} from "../lib/calendar";
import type { Hoist } from "../lib/config";
import { weekdayLabel } from "../lib/time";

type Placed = {
  id: string;
  start_at: string;
  end_at: string;
  node: ReactNode;
};

export function WeekHoistCalendars({
  base,
  weekStart,
  month,
  days,
  today,
  hoists,
  focusHoistId,
  itemsForHoist,
}: {
  base: "/schedule" | "/member/schedule";
  weekStart: string;
  month: string;
  days: string[];
  today: string;
  hoists: Hoist[];
  focusHoistId?: string;
  itemsForHoist: (hoist: Hoist, day: string) => Placed[];
}) {
  const hours = hourLabels();

  return (
    <div className="week-hoists">
      <nav className="hoist-jump" aria-label="Jump to hoist">
        {hoists.map((hoist) => (
          <a
            key={hoist.id}
            href={`#hoist-${hoist.id}`}
            className={focusHoistId === hoist.id ? "is-active" : undefined}
          >
            {hoistChipLabel(hoist.name, hoist.is_shop)}
            {hoist.is_shop ? <span className="muted"> · Owner-only</span> : null}
          </a>
        ))}
      </nav>
      {hoists.map((hoist) => (
        <section
          key={hoist.id}
          id={`hoist-${hoist.id}`}
          className={`hoist-week${focusHoistId === hoist.id ? " is-focus" : ""}${hoist.is_shop ? " hoist-week-shop" : ""}`}
        >
          <header className="hoist-week-head">
            <h2>{hoist.name}</h2>
            <div className="hoist-pills">
              {hoist.is_shop ? <span className="pill pill-shop">Owner-only</span> : null}
              <span className={`pill pill-${hoist.status}`}>{hoist.status}</span>
            </div>
          </header>
          <div className="hour-scroll">
            <div className="hour-grid">
              <div className="hour-corner">Hour</div>
              {days.map((day) => (
                <div key={day} className={`hour-day-head${day === today ? " is-today" : ""}`}>
                  {weekdayLabel(day)}
                </div>
              ))}
              <div className="hour-labels">
                {hours.map((label, index) => (
                  <div
                    key={label}
                    className={`hour-label${index >= OPEN_HOUR_START && index < OPEN_HOUR_END ? " is-open" : ""}`}
                  >
                    {label}
                  </div>
                ))}
              </div>
              {days.map((day) => {
                const items = itemsForHoist(hoist, day);
                return (
                  <div key={`${hoist.id}-${day}`} className={`hour-day${day === today ? " is-today" : ""}`}>
                    {hours.map((_, hour) => (
                      <Link
                        key={hour}
                        className={`hour-slot${hour >= OPEN_HOUR_START && hour < OPEN_HOUR_END ? " is-open" : ""}`}
                        href={scheduleHref(base, {
                          view: "week",
                          week: weekStart,
                          month,
                          hoist: hoist.id,
                          slot: `${day}T${String(hour).padStart(2, "0")}:00`,
                        })}
                        title={`Book ${hoist.name} ${day} ${String(hour).padStart(2, "0")}:00`}
                      >
                        <span className="sr-only">
                          {hoist.name} {day} {String(hour).padStart(2, "0")}:00
                        </span>
                      </Link>
                    ))}
                    {items.map((item) => {
                      const placement = bookingHourPlacement(item.start_at, item.end_at, day);
                      if (!placement) {
                        return null;
                      }
                      return (
                        <div
                          key={item.id}
                          className="hour-booking"
                          style={{ top: `${placement.topPct}%`, height: `${placement.heightPct}%` }}
                        >
                          {item.node}
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      ))}
    </div>
  );
}
