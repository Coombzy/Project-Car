"use client";

import { useEffect, useMemo, useState } from "react";

import { memberCreateBookingAction, memberRequestShopHoistAction } from "../app/member/schedule/actions";
import {
  balanceWouldGoNegative,
  bandAt,
  lowestFreeBay,
  selectionSummary,
  type BayChoice,
  type SpanInterval,
} from "../lib/booking-calendar";
import { CELL_WORD, NO_BAY_FREE_MESSAGE, TIME_LABEL } from "../lib/booking-words";
import { addDays, parseShopInstant, zonedDateTime, type ScheduleView } from "../lib/calendar";
import type { Hoist } from "../lib/config";
import { weekdayLabel } from "../lib/time";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";

export type CalendarSlot = SpanInterval & {
  id: string;
  own: boolean;
  name: string;
};

type Props = {
  view: ScheduleView;
  days: string[];
  today: string;
  nowIso: string;
  hoists: Hoist[];
  slots: CalendarSlot[];
  balance: string;
  returnTo: ScheduleReturn;
  error?: string | null;
};

type Anchor = { hoistId: string; day: string; hour: number };

const LANE_EDGE: Record<number, { color: string; style: string }> = {
  1: { color: "var(--accent)", style: "solid" },
  2: { color: "var(--ok)", style: "dotted" },
  3: { color: "var(--danger)", style: "dashed" },
  4: { color: "var(--text)", style: "double" },
  5: { color: "var(--muted)", style: "solid" },
  6: { color: "var(--line)", style: "solid" },
};

function pad(hour: number): string {
  return String(hour).padStart(2, "0");
}

function bayNumber(hoist: Hoist): number {
  if (hoist.is_shop) {
    return 6;
  }
  const match = hoist.name.match(/(\d+)/);
  return match ? Number(match[1]) : 99;
}

function bayChoice(hoist: Hoist): BayChoice {
  return {
    id: hoist.id,
    name: hoist.name,
    number: bayNumber(hoist),
    isShop: hoist.is_shop,
    status: hoist.status,
  };
}

function hourStart(day: string, hour: number): Date {
  return zonedDateTime(day, hour);
}

function slotCovers(slot: CalendarSlot, day: string, hour: number): boolean {
  const start = hourStart(day, hour).getTime();
  const end = hour === 23 ? zonedDateTime(addDays(day, 1), 0).getTime() : zonedDateTime(day, hour + 1).getTime();
  return parseShopInstant(slot.startAt).getTime() < end && parseShopInstant(slot.endAt).getTime() > start;
}

function wallStamp(day: string, hour: number): string {
  return `${day}T${pad(hour)}:00`;
}

function endStamp(day: string, hourExclusive: number): string {
  if (hourExclusive >= 24) {
    return `${addDays(day, 1)}T00:00`;
  }
  return wallStamp(day, hourExclusive);
}

export function BookingCalendar({ view, days, today, nowIso, hoists, slots, balance, returnTo, error }: Props) {
  const now = useMemo(() => new Date(nowIso), [nowIso]);
  const [showNight, setShowNight] = useState(false);
  const [lane, setLane] = useState<string>("all");
  const [day, setDay] = useState(days.includes(today) ? today : days[0] ?? today);
  const [anchor, setAnchor] = useState<Anchor | null>(null);
  const [focusHour, setFocusHour] = useState<number | null>(null);
  const [quoteTotal, setQuoteTotal] = useState<number | null>(null);
  const [quoteAfter, setQuoteAfter] = useState<number | null>(null);
  const [quoting, setQuoting] = useState(false);

  const choices = useMemo(() => hoists.map(bayChoice), [hoists]);
  const memberBays = choices.filter((bay) => !bay.isShop);

  const selection = useMemo(() => {
    if (!anchor || focusHour === null) {
      return null;
    }
    const selectedDay = anchor.day;
    const blocked = new Set<number>();
    const lo = Math.min(anchor.hour, focusHour);
    const hi = Math.max(anchor.hour, focusHour);
    for (let hour = lo; hour <= hi; hour += 1) {
      if (!hourIsFree(choices, slots, anchor.hoistId, selectedDay, hour, now)) {
        blocked.add(hour);
      }
    }
    const summary = selectionSummary(selectedDay, anchor.hour, focusHour + 1, blocked);
    const startAt = summary.hours.length === 0 ? "" : wallStamp(selectedDay, summary.hours[0] ?? anchor.hour);
    const endAt = summary.hours.length === 0 ? "" : endStamp(selectedDay, (summary.hours[summary.hours.length - 1] ?? anchor.hour) + 1);
    const bay =
      summary.hours.length === 0
        ? null
        : anchor.hoistId === "any"
          ? lowestFreeBay(choices, slots, startAt, endAt)
          : choices.find((item) => item.id === anchor.hoistId) ?? null;
    return { ...summary, day: selectedDay, hoistId: anchor.hoistId, bay, startAt, endAt };
  }, [anchor, choices, focusHour, now, slots]);

  const quoteKey = selection ? `${selection.startAt}|${selection.endAt}|${selection.bay?.id ?? ""}|${selection.bay?.isShop ? "shop" : "bay"}` : "";

  useEffect(() => {
    if (!selection || selection.hours.length === 0 || !selection.bay) {
      setQuoteTotal(null);
      setQuoteAfter(null);
      setQuoting(false);
      return;
    }
    if (selection.bay.isShop) {
      setQuoteTotal(0);
      setQuoteAfter(Number(balance));
      setQuoting(false);
      return;
    }
    const controller = new AbortController();
    setQuoting(true);
    const timer = window.setTimeout(async () => {
      try {
        const response = await fetch("/member/schedule/quote", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({ start_at: selection.startAt, end_at: selection.endAt }),
          signal: controller.signal,
        });
        const body = (await response.json()) as {
          reserved_tokens?: string;
          token_balance_after?: string | null;
        };
        if (!response.ok) {
          setQuoteTotal(null);
          setQuoteAfter(null);
          setQuoting(false);
          return;
        }
        setQuoteTotal(Number(body.reserved_tokens));
        setQuoteAfter(
          body.token_balance_after === null || body.token_balance_after === undefined
            ? null
            : Number(body.token_balance_after),
        );
        setQuoting(false);
      } catch (fetchError) {
        if ((fetchError as { name?: string }).name === "AbortError") {
          return;
        }
        setQuoting(false);
      }
    }, 200);
    return () => {
      controller.abort();
      window.clearTimeout(timer);
    };
  }, [balance, quoteKey, selection]);

  function pick(hoistId: string, pickedDay: string, hour: number) {
    setDay(pickedDay);
    if (!anchor || anchor.hoistId !== hoistId || anchor.day !== pickedDay) {
      setAnchor({ hoistId, day: pickedDay, hour });
      setFocusHour(hour);
      return;
    }
    setFocusHour(hour);
  }

  const hours = Array.from({ length: 24 }, (_, hour) => hour);
  const shownHoists = lane === "all" || lane === "any" ? hoists : hoists.filter((hoist) => hoist.id === lane);
  const responsive = view !== "day";
  const total = quoteTotal ?? selection?.total ?? 0;
  const after = quoteAfter ?? Number(balance) - total;
  const negative = selection ? balanceWouldGoNegative(balance, total) : false;
  const shop = selection?.bay?.isShop === true;
  const canBook = Boolean(selection && selection.hours.length > 0 && selection.bay && !quoting && !negative && (shop || quoteTotal !== null));

  return (
    <div className={`booking-cal${responsive ? " is-responsive" : ""}${showNight ? " show-night" : ""}`}>
      <style>{CALENDAR_CSS}</style>
      <p className="muted">
        Times are {TIME_LABEL}. A phone shows one day. A wide screen shows the week. Nothing is held until you book.
      </p>
      <div className="lane-row" role="toolbar" aria-label="Bays">
        <button type="button" className={lane === "all" ? "is-active" : ""} onClick={() => setLane("all")}>
          All
        </button>
        <button type="button" className={lane === "any" ? "is-active" : ""} onClick={() => { setLane("any"); setAnchor(null); }}>
          Any bay
        </button>
        {hoists.map((hoist) => (
          <button
            key={hoist.id}
            type="button"
            className={lane === hoist.id ? "is-active" : ""}
            onClick={() => setLane(hoist.id)}
          >
            {hoist.is_shop ? "Shop" : `B${bayNumber(hoist)}`}
          </button>
        ))}
      </div>
      <div className="day-pills" role="tablist" aria-label="Days">
        {days.map((item) => (
          <button
            key={item}
            type="button"
            role="tab"
            aria-selected={item === day}
            className={item === day ? "is-active" : ""}
            onClick={() => setDay(item)}
          >
            <span>{weekdayLabel(item)}</span>
            <span>{freeHours(memberBays, slots, item, now)}h free</span>
          </button>
        ))}
      </div>
      <button type="button" className="button ghost" onClick={() => setShowNight((value) => !value)}>
        {showNight ? "Hide night hours" : "Show night hours"}
      </button>
      <div className="day-layout">
        <LaneTable
          day={day}
          hours={hours}
          hoists={lane === "any" ? [] : shownHoists}
          anyBay={lane === "any"}
          choices={choices}
          slots={slots}
          now={now}
          selection={selection}
          onPick={pick}
          compact={false}
        />
      </div>
      <div className="week-layout">
        <WeekGrid
          days={days}
          hours={hours}
          hoists={lane === "any" ? [] : shownHoists}
          anyBay={lane === "any"}
          choices={choices}
          slots={slots}
          now={now}
          selection={selection}
          onPick={pick}
        />
      </div>
      <form
        className="booking-total"
        action={shop ? memberRequestShopHoistAction : memberCreateBookingAction}
        aria-live="polite"
      >
        <ScheduleReturnFields returnTo={returnTo} />
        <input type="hidden" name="hoist_id" value={selection?.bay?.id ?? ""} />
        <input type="hidden" name="start_at" value={selection?.startAt ?? ""} />
        <input type="hidden" name="end_at" value={selection?.endAt ?? ""} />
        {selection && selection.hours.length > 0 ? (
          <>
            <p>
              <strong>
                {selection.hoistId === "any" ? "Any bay" : selection.bay?.name ?? "Bay"} · {weekdayLabel(selection.day)}{" "}
                {pad(selection.hours[0] ?? 0)}:00–{pad((selection.hours[selection.hours.length - 1] ?? 0) + 1)}:00
              </strong>
            </p>
            <p>{quoting ? "Updating price…" : selection.line}</p>
            {selection.note ? <p>{selection.note}</p> : null}
            {selection.hoistId === "any" && selection.bay ? (
              <p>We'll put you on {selection.bay.name}, the lowest-numbered free bay. We check again when you book.</p>
            ) : null}
            {selection.hoistId === "any" && !selection.bay ? <p>{NO_BAY_FREE_MESSAGE}</p> : null}
            {shop ? <p>Shop hoist — ask first. A request does not hold the hour.</p> : null}
            {!shop && quoteAfter !== null ? (
              <p>
                Balance after {Number.isInteger(after) ? after : after.toFixed(2)} tokens.
              </p>
            ) : null}
            {negative ? <p role="alert">{`You need ${total} and have ${balance}. A balance can't go below zero.`}</p> : null}
          </>
        ) : (
          <p>Tap an open hour, then the last hour. The total stays here.</p>
        )}
        {error ? (
          <p role="alert">{error}</p>
        ) : null}
        <button className="button" type="submit" disabled={!canBook} aria-busy={quoting}>
          {quoting ? "Updating price…" : shop ? "Send request" : selection && selection.hours.length > 0 ? `Book ${selection.hours.length} h · ${total}` : "Book"}
        </button>
      </form>
    </div>
  );
}

function hourIsFree(
  choices: BayChoice[],
  slots: CalendarSlot[],
  hoistId: string,
  day: string,
  hour: number,
  now: Date,
): boolean {
  if (hourStart(day, hour).getTime() < now.getTime()) {
    return false;
  }
  if (hoistId === "any") {
    const startAt = wallStamp(day, hour);
    const endAt = endStamp(day, hour + 1);
    return lowestFreeBay(choices, slots, startAt, endAt) !== null;
  }
  const bay = choices.find((item) => item.id === hoistId);
  if (!bay || bay.status === "maintenance" || bay.status === "locked") {
    return false;
  }
  return !slots.some((slot) => slot.hoistId === hoistId && occupying(slot.status) && slotCovers(slot, day, hour));
}

function occupying(status: string): boolean {
  return status === "pending" || status === "confirmed" || status === "active" || status === "completed" || status === "overdue";
}

function freeHours(bays: BayChoice[], slots: CalendarSlot[], day: string, now: Date): number {
  let count = 0;
  for (const bay of bays) {
    for (let hour = 0; hour < 24; hour += 1) {
      if (hourIsFree([bay], slots, bay.id, day, hour, now)) {
        count += 1;
      }
    }
  }
  return count;
}

function WeekGrid({
  days,
  hours,
  hoists,
  anyBay,
  choices,
  slots,
  now,
  selection,
  onPick,
}: {
  days: string[];
  hours: number[];
  hoists: Hoist[];
  anyBay: boolean;
  choices: BayChoice[];
  slots: CalendarSlot[];
  now: Date;
  selection: { hours: number[]; day: string; hoistId: string } | null;
  onPick: (hoistId: string, day: string, hour: number) => void;
}) {
  const columns = anyBay ? [anyHoist()] : hoists;
  return (
    <div className="week-grid-lanes" role="grid" aria-label={`Week of bays, ${TIME_LABEL}`}>
      <div className="lane-row-hours" role="row">
        <div className="gutter" />
        {days.map((item) => (
          <div key={item} className="day-bays day-name">
            {weekdayLabel(item)}
          </div>
        ))}
      </div>
      {hours.map((hour) => {
        return (
          <div key={hour} className={`lane-row-hours${hour < 6 ? " night" : ""}`} role="row">
            <div className="gutter">{`${pad(hour)}:00`}</div>
            {days.map((item) => (
              <div key={item} className="day-bays" role="presentation">
                {columns.map((hoist) => {
                  const hoistId = anyBay ? "any" : hoist.id;
                  const picked = Boolean(
                    selection && selection.hoistId === hoistId && selection.day === item && selection.hours.includes(hour),
                  );
                  const text = cellText(choices, slots, hoist, anyBay, item, hour, now, picked, true);
                  return (
                    <button
                      key={`${item}-${hoist.id}`}
                      type="button"
                      role="gridcell"
                      className={`lane-cell${picked ? " is-picked" : ""}`}
                      style={edgeStyle(anyBay ? 0 : bayNumber(hoist))}
                      aria-label={text.aria}
                      disabled={!text.selectable}
                      onClick={() => onPick(hoistId, item, hour)}
                    >
                      {text.visible}
                    </button>
                  );
                })}
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
}

function anyHoist(): Hoist {
  return {
    id: "any",
    name: "Any bay",
    location_label: "",
    status: "available",
    is_shop: false,
    created_at: "",
    updated_at: "",
  };
}

function LaneTable({
  day,
  hours,
  hoists,
  anyBay,
  choices,
  slots,
  now,
  selection,
  onPick,
  compact,
}: {
  day: string;
  hours: number[];
  hoists: Hoist[];
  anyBay: boolean;
  choices: BayChoice[];
  slots: CalendarSlot[];
  now: Date;
  selection: { hours: number[]; day: string; hoistId: string } | null;
  onPick: (hoistId: string, day: string, hour: number) => void;
  compact: boolean;
}) {
  const columns = anyBay ? [anyHoist()] : hoists;
  return (
    <div className="lane-table" role="grid" aria-label={`${weekdayLabel(day)}, ${TIME_LABEL}`}>
      {hours.map((hour) => {
        const band = bandAt(day, hour);
        const previous = hour === 0 ? null : bandAt(day, hour - 1);
        return (
          <div key={hour} className={`lane-row-hours${hour < 6 ? " night" : ""}`} role="row">
            <div className="gutter">
              {previous?.id !== band.id ? band.gutter : `${pad(hour)}:00`}
            </div>
            {columns.map((hoist) => {
              const hoistId = anyBay ? "any" : hoist.id;
              const picked = Boolean(
                selection && selection.hoistId === hoistId && selection.day === day && selection.hours.includes(hour),
              );
              const text = cellText(choices, slots, hoist, anyBay, day, hour, now, picked, compact);
              return (
                <button
                  key={hoist.id}
                  type="button"
                  role="gridcell"
                  className={`lane-cell${picked ? " is-picked" : ""}`}
                  style={edgeStyle(anyBay ? 0 : bayNumber(hoist))}
                  aria-label={text.aria}
                  disabled={!text.selectable}
                  onClick={() => onPick(hoistId, day, hour)}
                >
                  {text.visible}
                </button>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}

function edgeStyle(number: number): { borderLeft: string } {
  const edge = LANE_EDGE[number] ?? { color: "var(--line)", style: "solid" };
  return { borderLeft: `4px ${edge.style} ${edge.color}` };
}

function cellText(
  choices: BayChoice[],
  slots: CalendarSlot[],
  hoist: Hoist,
  anyBay: boolean,
  day: string,
  hour: number,
  now: Date,
  picked: boolean,
  compact: boolean,
): { visible: string; aria: string; selectable: boolean } {
  const band = bandAt(day, hour);
  const when = `${weekdayLabel(day)} ${pad(hour)}:00, ${band.gutter}, ${TIME_LABEL}`;
  if (hourStart(day, hour).getTime() < now.getTime()) {
    return { visible: CELL_WORD.past, aria: `${when}, past`, selectable: false };
  }
  if (anyBay) {
    const startAt = wallStamp(day, hour);
    const endAt = endStamp(day, hour + 1);
    const free = lowestFreeBay(choices, slots, startAt, endAt);
    const openCount = choices.filter((bay) => !bay.isShop && hourIsFree(choices, slots, bay.id, day, hour, now)).length;
    const memberCount = choices.filter((bay) => !bay.isShop).length;
    if (picked) {
      return { visible: CELL_WORD.picked, aria: `${when}, picked`, selectable: true };
    }
    if (!free) {
      return { visible: `0 of ${memberCount}`, aria: `${when}, full`, selectable: false };
    }
    return {
      visible: compact ? `${openCount}/${memberCount}` : `${openCount} of ${memberCount} free`,
      aria: `${when}, ${openCount} of ${memberCount} bays free`,
      selectable: true,
    };
  }
  const covered = slots.find((slot) => slot.hoistId === hoist.id && occupying(slot.status) && slotCovers(slot, day, hour));
  if (covered) {
    const word = covered.own ? CELL_WORD.yours : covered.status === "pending" ? CELL_WORD.held : CELL_WORD.booked;
    return { visible: compact && word === CELL_WORD.booked ? "Bkd" : word, aria: `${hoist.name}, ${when}, ${word}`, selectable: false };
  }
  if (hoist.status === "maintenance" || hoist.status === "locked") {
    return { visible: CELL_WORD.closed, aria: `${hoist.name}, ${when}, closed`, selectable: false };
  }
  if (hoist.is_shop) {
    return {
      visible: picked ? CELL_WORD.picked : compact ? "Ask" : CELL_WORD.ask,
      aria: `${hoist.name}, ${when}, ask first`,
      selectable: true,
    };
  }
  if (picked) {
    return { visible: CELL_WORD.picked, aria: `${hoist.name}, ${when}, picked`, selectable: true };
  }
  const open = `Open ${band.tokens}`;
  return { visible: compact ? String(band.tokens) : open, aria: `${hoist.name}, ${when}, open`, selectable: true };
}

const CALENDAR_CSS = `
.booking-cal { display: flex; flex-direction: column; gap: 12px; }
.booking-cal .lane-row, .booking-cal .day-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.booking-cal .lane-row button, .booking-cal .day-pills button, .booking-cal .lane-cell {
  min-height: 44px;
  font: inherit;
  color: var(--text);
  background: var(--bg-input);
  border: 1px solid var(--line);
  border-radius: 6px;
}
.booking-cal .is-active { outline: 2px solid var(--accent); }
.booking-cal .day-pills button { display: flex; flex-direction: column; align-items: flex-start; padding: 8px; }
.booking-cal .lane-table { display: flex; flex-direction: column; gap: 4px; }
.booking-cal .lane-row-hours { display: flex; gap: 4px; align-items: stretch; }
.booking-cal .gutter { width: 4.5rem; flex: none; font-size: 13px; align-self: center; }
.booking-cal .lane-cell { flex: 1; min-width: 0; font-size: 13px; text-align: left; padding: 4px 6px; }
.booking-cal .lane-cell:disabled { color: var(--muted); }
.booking-cal .is-picked { background: var(--bg-elev); outline: 2px solid var(--accent); }
.booking-cal .night { display: none; }
.booking-cal.show-night .night { display: flex; }
.booking-cal .week-layout { display: none; }
.booking-cal.is-responsive .day-layout { display: block; }
@media (min-width: 768px) {
  .booking-cal.is-responsive .day-layout { display: none; }
  .booking-cal.is-responsive .week-layout { display: block; }
  .booking-cal .day-bays { flex: 1; display: flex; gap: 2px; min-width: 0; }
  .booking-cal .day-name { font-size: 13px; align-items: center; }
}
.booking-total {
  position: sticky;
  bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: var(--bg-elev);
  border: 1px solid var(--line);
  border-radius: 10px;
  box-shadow: var(--shadow);
}
.booking-total .button { min-height: 48px; }
.booking-total .button:disabled { opacity: 0.55; }
`;
