import type { CalendarStatus } from "../lib/config";

export function CalendarConnect({ calendar }: { calendar: CalendarStatus | null }) {
  if (!calendar) {
    return (
      <div className="banner empty">
        Calendar connect is unavailable. Download an ICS from a to-do due date.
      </div>
    );
  }
  return (
    <div className="calendar-connect card">
      <div className="hoist-card-head">
        <h3>Calendars</h3>
        <span className="pill pill-pending">Stub</span>
      </div>
      <p className="muted">
        Two-way Google sync is not configured. Apple Calendar imports an ICS.
        Time zone is America/Regina.
      </p>
      <div className="actions">
        <button type="button" disabled title={calendar.next}>
          {calendar.google.label}
        </button>
        <button type="button" disabled title={calendar.apple.hint ?? calendar.next}>
          Connect Apple Calendar
        </button>
      </div>
      <p className="muted">{calendar.next}</p>
    </div>
  );
}
