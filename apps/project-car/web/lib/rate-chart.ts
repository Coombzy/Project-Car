/** Colours for the member rate chart. Tokens come from the saved bands. */

export const PEAK_CAP_NOTE = "Only Peak counts toward the 4-hour weekly cap.";

export type RateBand = {
  id: string;
  label: string;
  multiplier: string;
  tokens_per_hour: string;
};

export type RateHour = {
  weekday: number;
  day_label: string;
  hour: number;
  band_id: string;
  label: string;
  tokens_per_hour: string;
  counts_toward_peak_cap: boolean;
};

export type RateChartData = {
  tz_label: string;
  peak_cap_hours: number;
  note: string;
  bands: RateBand[];
  hours: RateHour[];
};

export function cellColour(bandId: string): string {
  switch (bandId) {
    case "late_night":
      return "#6e7988";
    case "weekday_day":
      return "#9fd19a";
    case "weekday_eve":
      return "#c084fc";
    case "weekend_fri_eve":
      return "#e8a54b";
    default:
      return "#f3f0e8";
  }
}
