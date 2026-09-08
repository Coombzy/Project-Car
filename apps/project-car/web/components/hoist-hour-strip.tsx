import Link from "next/link";

import type { BookedHour, HoistSnapshot } from "../lib/config";
import { formatShopTime } from "../lib/time";
import { StatusPill } from "./status-pill";

function groupHours(hours: BookedHour[]): BookedHour[][] {
  const groups: BookedHour[][] = [];
  for (const hour of hours) {
    const last = groups[groups.length - 1];
    const prev = last?.[last.length - 1];
    if (prev && prev.booking_id === hour.booking_id && prev.hour_end === hour.hour_start) {
      last.push(hour);
    } else {
      groups.push([hour]);
    }
  }
  return groups;
}

export function HoistHourStrip({
  hoist,
  scheduleHref,
  linkMembers = true,
}: {
  hoist: HoistSnapshot;
  scheduleHref: string;
  linkMembers?: boolean;
}) {
  const groups = groupHours(hoist.next_hours);
  const empty = groups.length === 0;
  return (
    <article
      className={`card hoist-card${hoist.is_shop ? " hoist-card-shop" : ""}${empty ? " hoist-card-empty" : " hoist-card-booked"}`}
    >
      <div className="hoist-card-head">
        <div>
          <h3>{hoist.name}</h3>
          <p className="muted hoist-location">{hoist.location_label || "No location label"}</p>
        </div>
        <div className="hoist-pills">
          {hoist.is_shop ? <StatusPill value="shop" /> : null}
          <StatusPill value={hoist.status} />
        </div>
      </div>
      {empty ? (
        <div className="banner empty hoist-empty">Clear next 24 hours</div>
      ) : (
        <ol className="hour-strip">
          {groups.map((group) => {
            const first = group[0];
            const last = group[group.length - 1];
            return (
              <li key={`${first.booking_id}-${first.hour_start}`} className="hour-strip-item">
                <div className="hour-strip-when">
                  <strong>
                    {formatShopTime(first.hour_start)}–{formatShopTime(last.hour_end)}
                  </strong>
                  <span className="muted">
                    {group.length} booked hour{group.length === 1 ? "" : "s"}
                  </span>
                </div>
                <div>
                  {first.member_id && linkMembers ? (
                    <Link href={`/members/${first.member_id}`}>{first.member_name}</Link>
                  ) : (
                    <strong>{first.member_name}</strong>
                  )}
                  <div className="muted">{first.vehicle_label}</div>
                </div>
                <StatusPill value={first.status} />
              </li>
            );
          })}
        </ol>
      )}
      <p>
        <Link href={scheduleHref}>Open this bay on the schedule →</Link>
      </p>
    </article>
  );
}
