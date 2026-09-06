import type { ReactNode } from "react";

export function PlaceholderNote({ children }: { children: ReactNode }) {
  return <div className="banner demo">{children}</div>;
}
