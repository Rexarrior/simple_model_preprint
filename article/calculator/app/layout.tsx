import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

/* eslint-disable @next/next/no-sync-scripts */

const title = "M4 Workbench — human–agent planning calculator";
const description = "Estimate development speedup, the critical path, and human-attention load locally with the M4 model.";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host") ?? "localhost";
  const protocol = requestHeaders.get("x-forwarded-proto") ?? (host.startsWith("localhost") ? "http" : "https");
  const base = new URL(`${protocol}://${host}`);
  const socialImage = new URL("/og.png", base).toString();
  return {
    metadataBase: base,
    title,
    description,
    icons: { icon: "/favicon.png", shortcut: "/favicon.png" },
    openGraph: { title, description, type: "website", images: [{ url: socialImage, width: 1680, height: 945 }] },
    twitter: { card: "summary_large_image", title, description, images: [socialImage] },
  };
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="color-scheme" content="light dark" />
        <meta name="theme-color" content="#f3f1ea" />
        <script src="/theme-init.js" />
      </head>
      <body>{children}</body>
    </html>
  );
}
