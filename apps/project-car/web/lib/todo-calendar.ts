const CALENDAR_TZ = "America/Regina";

export type TodoDue = {
  title: string;
  notes: string | null;
  due_at: string | null;
};

function pad(value: number): string {
  return String(value).padStart(2, "0");
}

function googleUtcStamp(iso: string): string {
  const date = new Date(iso);
  return `${date.getUTCFullYear()}${pad(date.getUTCMonth() + 1)}${pad(date.getUTCDate())}T${pad(date.getUTCHours())}${pad(date.getUTCMinutes())}00Z`;
}

export function googleTemplateUrl(todo: TodoDue): string | null {
  if (!todo.due_at) {
    return null;
  }
  const start = googleUtcStamp(todo.due_at);
  const endDate = new Date(new Date(todo.due_at).getTime() + 60 * 60 * 1000);
  const end = `${endDate.getUTCFullYear()}${pad(endDate.getUTCMonth() + 1)}${pad(endDate.getUTCDate())}T${pad(endDate.getUTCHours())}${pad(endDate.getUTCMinutes())}00Z`;
  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: todo.title,
    dates: `${start}/${end}`,
    details: todo.notes ?? "Project Car Shop OS to-do",
    ctz: CALENDAR_TZ,
  });
  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

export function partsStatusLabel(status: string): string {
  if (status === "in_transit") {
    return "In transit";
  }
  return status.replace("_", " ");
}
