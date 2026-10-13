import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./globals.css";

export const metadata: Metadata = {
  title: "ScamShield OSS — Stop. Check. Stay safe.",
  description:
    "Local-first scam analysis for suspicious messages, screenshots, job offers, and URLs.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
