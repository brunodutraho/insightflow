import type { Metadata } from "next";
import "./globals.css";
import Providers from "./providers";

export const metadata: Metadata = {
  title: "InsightFlow",
  description: "Marketing Analytics SaaS",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt">
      <body className="bg-slate-950 text-white">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
