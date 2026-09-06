import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Project Car · Shop OS",
  description: "Project Car management demo — Owner admin. Member /member is a temporary park, not the permanent customer app.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
