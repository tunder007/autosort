/**
 * layout.tsx — app shell with navigation.
 *
 * What it does:
 *   Root layout, global styles, nav links to Sort / History / Connect / API docs.
 *
 * Does not:
 *   Handle auth or API calls.
 */
import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Autosort",
  description: "Sort files by type — pay as you go",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main>
          <nav>
            <Link href="/sort">Sort</Link>
            <Link href="/history">History</Link>
            <Link href="/connect">Connect</Link>
            <a href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`} target="_blank" rel="noreferrer">
              API Docs
            </a>
          </nav>
          {children}
        </main>
      </body>
    </html>
  );
}
