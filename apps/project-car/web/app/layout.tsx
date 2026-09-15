import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Project Car · Shop OS",
  description: "Project Car management demo (ops.projectcar.ca LIVE; app.projectcar.ca temporary alias). Member /member is a temporary park. Customer app is projectcar.ca.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
