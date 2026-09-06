import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Project Car · Shop OS",
  description: "Owner shop OS demo for Project Car members, hoists, and bookings.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
