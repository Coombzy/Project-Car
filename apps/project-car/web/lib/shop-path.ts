export function pathSegment(value: string): string {
  if (value === "" || value === "." || value === "..") {
    throw new Error("Bad path segment.");
  }
  return encodeURIComponent(value);
}
