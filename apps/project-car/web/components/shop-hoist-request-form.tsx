"use client";

import { useState } from "react";

import { memberRequestShopHoistAction } from "../app/member/schedule/actions";
import type { Hoist } from "../lib/config";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";

type Props = {
  hoist: Hoist;
  weekStart: string;
  defaultStart: string;
  defaultEnd: string;
  returnTo: ScheduleReturn;
};

export function ShopHoistRequestForm({ hoist, weekStart, defaultStart, defaultEnd, returnTo }: Props) {
  const [startAt, setStartAt] = useState(defaultStart);
  const [endAt, setEndAt] = useState(defaultEnd);

  return (
    <form action={memberRequestShopHoistAction} className="stack-form" id="request-shop-hoist">
      <ScheduleReturnFields returnTo={returnTo} />
      <input type="hidden" name="week" value={weekStart} />
      <input type="hidden" name="hoist_id" value={hoist.id} />
      <p className="muted">
        {hoist.name} stays pending until a person or an AI approves it. This does not book the
        hour and does not use tokens.
      </p>
      <div className="form-grid">
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
      <div className="actions">
        <button type="submit">Request the shop hoist</button>
      </div>
    </form>
  );
}
