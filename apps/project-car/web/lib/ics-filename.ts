/** Safe Content-Disposition for an owner or member to-do ICS download. */

const FALLBACK_NAME = "todo.ics";

function safeIcsName(filename: string): string {
  const segments = filename.replace(/[\u0000-\u001F\u007F"']/g, "").split(/[/\\]/);
  let base = "";
  for (const segment of segments) {
    if (segment.length > 0) {
      base = segment;
    }
  }
  const ascii = base.replace(/[^A-Za-z0-9._-]/g, "");
  const stemSource = ascii.toLowerCase().endsWith(".ics") ? ascii.slice(0, -4) : ascii;
  const stem = stemSource.replace(/^[^A-Za-z0-9]+/, "").replace(/[^A-Za-z0-9]+$/, "");
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(stem)) {
    return FALLBACK_NAME;
  }
  return `${stem}.ics`;
}

export function contentDispositionForIcs(filename: string): string {
  return `attachment; filename="${safeIcsName(filename)}"`;
}
