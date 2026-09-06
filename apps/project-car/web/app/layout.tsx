import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Project Car · Shop OS",
  description: "Shop OS demo for Project Car — Owner admin and Member self-serve booking.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
