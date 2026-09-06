"use client";

import { useEffect, useState } from "react";

import { createBookingAction } from "../app/schedule/actions";
import type { BookingQuote, Hoist, Member } from "../lib/config";
import { tokensLabel } from "../lib/time";

type Props = {
  members: Member[];
  hoists: Hoist[];
  weekStart: string;
  defaultStart: string;
  defaultEnd: string;
};

export function CreateBookingForm({ members, hoists, weekStart, defaultStart, defaultEnd }: Props) {
  const [kind, setKind] = useState<"customer" | "shop">("customer");
  const [memberId, setMemberId] = useState(members[0]?.id ?? "");
  const [startAt, setStartAt] = useState(defaultStart);
  const [endAt, setEndAt] = useState(defaultEnd);
  const [quote, setQuote] = useState<BookingQuote | null>(null);
  const [quoteError, setQuoteError] = useState<string | null>(null);
  const shopHoist = hoists.find((hoist) => hoist.is_shop);
  const hoistChoices = kind === "shop" ? hoists.filter((hoist) => hoist.is_shop) : hoists.filter((hoist) => !hoist.is_shop);

  useEffect(() => {
    if (kind === "shop" || !startAt || !endAt) {
      setQuote(null);
      setQuoteError(null);
      return;
    }
    const controller = new AbortController();
    const timer = window.setTimeout(async () => {
      try {
        const response = await fetch("/schedule/quote", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            start_at: startAt,
            end_at: endAt,
            member_id: memberId || undefined,
          }),
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
  }, [startAt, endAt, memberId, kind]);

  const selected = members.find((member) => member.id === memberId);
  const rule = quote?.pricing_rule;

  return (
    <form action={createBookingAction} className="stack-form">
      <input type="hidden" name="week" value={weekStart} />
      <div className="form-grid">
        <label>
          Kind
          <select name="kind" value={kind} onChange={(event) => setKind(event.target.value as "customer" | "shop")}>
            <option value="customer">Customer</option>
            <option value="shop">Shop work</option>
          </select>
        </label>
        <label>
          Member
          <select
            name="member_id"
            required={kind === "customer"}
            value={kind === "shop" ? "" : memberId}
            onChange={(event) => setMemberId(event.target.value)}
          >
            {kind === "shop" ? <option value="">Shop (no member)</option> : null}
            {members.map((member) => (
              <option key={member.id} value={member.id}>
                {member.name} · {member.tier_name} · {member.token_balance} tok
              </option>
            ))}
          </select>
        </label>
        <label>
          Hoist
          <select
            name="hoist_id"
            required
            defaultValue={kind === "shop" ? shopHoist?.id : hoistChoices[0]?.id}
            key={kind}
          >
            {hoistChoices.map((hoist) => (
              <option key={hoist.id} value={hoist.id}>
                {hoist.name}
                {hoist.is_shop ? " · shop hoist · Owner-only" : ""} · {hoist.status}
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
      {kind === "shop" ? (
        <p className="muted">
          Shop work is Owner-only on the shop hoist (v1 choice A). Customers
          cannot book this bay. No member tokens reserved.
        </p>
      ) : rule ? (
        <div className="quote-preview">
          <p className="eyebrow">Reserve quote · America/Regina bands</p>
          <p className="quote-math">
            {rule.hours}h × 100 × {rule.band_multiplier} × {rule.advance_multiplier} ={" "}
            <strong>{tokensLabel(rule.final_reserve_cost)}</strong>
          </p>
          <p className="muted">
            {tokensLabel(rule.base_tokens)} base · {rule.band_label} · {rule.overlay_label}
          </p>
          {quote?.token_balance !== null && quote?.token_balance_after !== null ? (
            <p className="muted">
              {selected?.name ?? "Member"} balance {tokensLabel(quote.token_balance)} →{" "}
              {tokensLabel(quote.token_balance_after)}
            </p>
          ) : null}
        </div>
      ) : quoteError ? (
        <p className="muted">{quoteError}</p>
      ) : (
        <p className="muted">Pick a start and end to see duration × band × overlay.</p>
      )}
      <div className="actions">
        <button type="submit">Reserve booking</button>
      </div>
    </form>
  );
}
