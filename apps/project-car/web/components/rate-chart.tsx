import Link from "next/link";

import { cellColour, type RateChartData } from "../lib/rate-chart";

export type { RateChartData };

const HOURS = Array.from({ length: 24 }, (_, hour) => hour);

export function RateChart({
  rates,
  helpHref,
}: {
  rates: RateChartData;
  helpHref?: string;
}) {
  const days = [...new Set(rates.hours.map((hour) => hour.weekday))];
  return (
    <section className="card rate-chart" aria-labelledby="rate-chart-title" style={{ marginTop: "1rem" }}>
      <div className="hoist-card-head">
        <h2 id="rate-chart-title" style={{ marginTop: 0 }}>
          Weekly rates
        </h2>
        {helpHref ? <Link href={helpHref}>How rates work</Link> : null}
      </div>
      <p className="muted">
        7 days × 24 hours, {rates.tz_label}. Each square is one hour.
      </p>
      <div style={{ overflowX: "auto" }}>
        <table style={{ borderCollapse: "separate", borderSpacing: "2px", minWidth: "100%" }}>
          <caption className="muted" style={{ textAlign: "left", marginBottom: "0.4rem" }}>
            Shop week in {rates.tz_label}
          </caption>
          <thead>
            <tr>
              <th scope="col" style={{ textAlign: "left", color: "var(--text)", fontWeight: 600 }}>
                Day
              </th>
              {HOURS.map((hour) => (
                <th
                  key={hour}
                  scope="col"
                  style={{
                    color: "var(--text)",
                    fontWeight: 500,
                    fontSize: "0.68rem",
                    minWidth: "1.35rem",
                    textAlign: "center",
                  }}
                >
                  {hour}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {days.map((weekday) => {
              const row = rates.hours
                .filter((hour) => hour.weekday === weekday)
                .sort((left, right) => left.hour - right.hour);
              const label = row[0]?.day_label ?? "";
              return (
                <tr key={weekday}>
                  <th
                    scope="row"
                    style={{
                      textAlign: "left",
                      color: "var(--text)",
                      background: "var(--bg-elev)",
                      position: "sticky",
                      left: 0,
                      paddingRight: "0.6rem",
                      fontWeight: 600,
                    }}
                  >
                    {label}
                  </th>
                  {row.map((hour) => (
                    <td
                      key={hour.hour}
                      title={`${label} ${hour.hour}:00, ${hour.label}, ${hour.tokens_per_hour} tokens/hr`}
                      style={{
                        background: cellColour(hour.band_id),
                        position: "relative",
                        width: "1.35rem",
                        height: "1.35rem",
                        padding: 0,
                        borderRadius: "2px",
                      }}
                    >
                      <span
                        style={{
                          position: "absolute",
                          width: "1px",
                          height: "1px",
                          overflow: "hidden",
                          clip: "rect(0 0 0 0)",
                        }}
                      >
                        {label} {hour.hour}:00 {hour.label} {hour.tokens_per_hour} tokens per hour
                      </span>
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <ul style={{ display: "flex", flexWrap: "wrap", gap: "0.8rem 1.2rem", listStyle: "none", padding: 0 }}>
        {rates.bands.map((band) => (
          <li key={band.id} style={{ display: "flex", alignItems: "center", gap: "0.45rem", color: "var(--text)" }}>
            <span
              aria-hidden="true"
              style={{
                width: "0.95rem",
                height: "0.95rem",
                borderRadius: "2px",
                background: cellColour(band.id),
                display: "inline-block",
              }}
            />
            <span>
              {band.label} · {band.tokens_per_hour} tokens/hr
            </span>
          </li>
        ))}
      </ul>
      <p style={{ color: "var(--text)", marginBottom: 0 }}>{rates.note}</p>
    </section>
  );
}
