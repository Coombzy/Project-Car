export type ScheduleReturn = {
  view: string;
  week: string;
  month: string;
  hoist?: string;
};

export function ScheduleReturnFields({ returnTo }: { returnTo: ScheduleReturn }) {
  return (
    <>
      <input type="hidden" name="view" value={returnTo.view} />
      <input type="hidden" name="week" value={returnTo.week} />
      <input type="hidden" name="month" value={returnTo.month} />
      {returnTo.hoist ? <input type="hidden" name="hoist" value={returnTo.hoist} /> : null}
    </>
  );
}
