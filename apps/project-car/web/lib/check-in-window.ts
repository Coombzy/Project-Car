/** Stand-in. Matches CHECK_IN_EARLY_MINUTES in the shop API bookings service. */
export const CHECK_IN_EARLY_MINUTES = 15;

export const CHECK_IN_EARLY_HINT = "Opens 15 min before start";

export type CheckInButtonState = {
  disabled: boolean;
  hint: string | null;
};

export function checkInButtonState(startAt: string, now: Date): CheckInButtonState {
  const startMs = new Date(startAt).getTime();
  const tooEarly =
    Number.isFinite(startMs) && startMs - now.getTime() > CHECK_IN_EARLY_MINUTES * 60 * 1000;
  if (!tooEarly) {
    return { disabled: false, hint: null };
  }
  return { disabled: true, hint: CHECK_IN_EARLY_HINT };
}
