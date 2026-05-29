import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ReconCore Dashboard",
  description: "Monitoring and reconciliation dashboard for ReconCore."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

