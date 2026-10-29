import Link from "next/link";

import type { Booking } from "../lib/config";
import { nextVisit, NO_VISIT_BOOKED, SCHEDULE_HREF } from "../lib/next-visit";
import { StatusPill } from "./status-pill";

export function NextVisitCard({
  bookings,
  now,
}: {
  bookings: readonly Booking[];
  now: Date;
}) {
  const visit = nextVisit(bookings, now);
  return (
    <section aria-labelledby="next-visit-heading">
      <h2 id="next-visit-heading">Next visit</h2>
      {visit ? (
        <div className="card">
          <p>
            <b>{visit.bay}</b>
          </p>
          <p>
            {visit.dayLabel} · {visit.timeLabel}
          </p>
          <p>
            <StatusPill value={visit.status} />
          </p>
          <p>{visit.checkInOpensLabel}</p>
        </div>
      ) : (
        <div className="banner empty">
          <Link href={SCHEDULE_HREF}>{NO_VISIT_BOOKED}</Link>
        </div>
      )}
    </section>
  );
}
