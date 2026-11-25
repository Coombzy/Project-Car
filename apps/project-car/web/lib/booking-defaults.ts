/** STAND-IN from R108 until Ben confirms the member duration cap. */
export const MAX_MEMBER_BOOKING_HOURS = 12;

/** STAND-IN from R108 until Ben confirms the shop duration cap. */
export const MAX_SHOP_BOOKING_HOURS = 24;

/** Next whole local hour. 19:59 becomes 20:00; an exact hour stays put. */
export function nextHourStart(now: Date): Date {
  const start = new Date(now.getTime());
  if (start.getMinutes() === 0 && start.getSeconds() === 0 && start.getMilliseconds() === 0) {
    return start;
  }
  start.setHours(start.getHours() + 1, 0, 0, 0);
  return start;
}

/** Start plus a whole number of hours, in 1..MAX_SHOP_BOOKING_HOURS. */
export function endFromDuration(start: Date, hours: number): Date {
  const end = new Date(start.getTime());
  end.setHours(end.getHours() + hours);
  return end;
}
