import type { ReactNode } from "react";

export function Banner({
  children,
  tone,
}: {
  children: ReactNode;
  tone?: "error" | "empty" | "demo";
}) {
  const className = tone ? `banner ${tone}` : "banner";
  return (
    <div className={className} role="alert">
      {children}
    </div>
  );
}
