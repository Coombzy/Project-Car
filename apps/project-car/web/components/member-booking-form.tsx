"use client";

import { useEffect, useState } from "react";

import { memberCreateBookingAction } from "../app/member/schedule/actions";
import type { BookingQuote, Hoist, MemberSelf } from "../lib/config";
import { tokensLabel } from "../lib/time";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";

type Props = {
  member: MemberSelf;
  hoists: Hoist[];
  weekStart: string;
  defaultStart: string;
  defaultEnd: string;
  defaultHoistId?: string;
  returnTo: ScheduleReturn;
};

export function MemberBookingForm({
  member,
  hoists,
  weekStart,
  defaultStart,
  defaultEnd,
  defaultHoistId,
  returnTo,
}: Props) {
  const [startAt, setStartAt] = useState(defaultStart);
  const [endAt, setEndAt] = useState(defaultEnd);
  const [quote, setQuote] = useState<BookingQuote | null>(null);
  const [quoteError, setQuoteError] = useState<string | null>(null);
  const bays = hoists.filter((hoist) => !hoist.is_shop);

  useEffect(() => {
    if (!startAt || !endAt) {
      setQuote(null);
      setQuoteError(null);
      return;
    }
    const controller = new AbortController();
    const timer = window.setTimeout(async () => {
      try {
        const response = await fetch("/member/schedule/quote", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({ start_at: startAt, end_at: endAt }),
          signal: controller.signal,
        });
        const body = (await response.json()) as BookingQuote & {
          error?: { message?: string };
        };
        if (!response.ok) {
          setQuote(null);
          setQuoteError(body.error?.message ?? "Could not quote this window.");
          return;
        }
        setQuoteError(null);
        setQuote(body);
      } catch (error) {
        if ((error as { name?: string }).name === "AbortError") {
          return;
        }
        setQuote(null);
        setQuoteError("Could not quote this window.");
      }
    }, 200);
    return () => {
      controller.abort();
      window.clearTimeout(timer);
    };
  }, [startAt, endAt]);

  const rule = quote?.pricing_rule;

  return (
    <form action={memberCreateBookingAction} className="stack-form" id="create-booking">
      <ScheduleReturnFields returnTo={returnTo} />
      <input type="hidden" name="week" value={weekStart} />
      <div className="form-grid">
        <label>
          Bay
          <select
            name="hoist_id"
            required
            defaultValue={bays.some((hoist) => hoist.id === defaultHoistId) ? defaultHoistId : bays[0]?.id}
          >
            {bays.map((hoist) => (
              <option key={hoist.id} value={hoist.id}>
                {hoist.name} · {hoist.status}
              </option>
            ))}
          </select>
        </label>
        <label>
          Start
          <input
            type="datetime-local"
            name="start_at"
            required
            value={startAt}
            onChange={(event) => setStartAt(event.target.value)}
          />
        </label>
        <label>
          End
          <input
            type="datetime-local"
            name="end_at"
            required
            value={endAt}
            onChange={(event) => setEndAt(event.target.value)}
          />
        </label>
        <label>
          Notes
          <input type="text" name="notes" placeholder="Optional" />
        </label>
      </div>
      {rule ? (
        <div className="quote-preview">
          <p className="eyebrow">Reserve quote · America/Regina bands</p>
          <p className="quote-math">
            {rule.hours}h × 100 × {rule.band_multiplier} × {rule.advance_multiplier}
            {rule.fill_multiplier && rule.fill_multiplier !== "1" ? ` × ${rule.fill_multiplier}` : ""} ={" "}
            <strong>{tokensLabel(rule.final_reserve_cost)}</strong>
          </p>
          <p className="muted">
            {tokensLabel(rule.base_tokens)} base · {rule.band_label} · {rule.overlay_label}
            {rule.fill_multiplier && rule.fill_multiplier !== "1" ? ` · ${rule.fill_label ?? "Fill"}` : ""}
          </p>
          {quote?.token_balance !== null && quote?.token_balance_after !== null ? (
            <p className="muted">
              {member.name} balance {tokensLabel(quote.token_balance)} →{" "}
              {tokensLabel(quote.token_balance_after)}
            </p>
          ) : null}
        </div>
      ) : quoteError ? (
        <p className="muted">{quoteError}</p>
      ) : (
        <p className="muted">Pick a start and end to see duration × band × overlay × fill.</p>
      )}
      <div className="actions">
        <button type="submit">Book and confirm</button>
      </div>
    </form>
  );
}
