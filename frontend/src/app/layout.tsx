import type { Metadata } from "next";
import { Inter, Roboto } from "next/font/google"; // Importação das fontes
import "./globals.css";
import Providers from "./providers";

// Configuração da Inter (Principal para UI)
const inter = Inter({ 
  subsets: ["latin"], 
  variable: "--font-inter",
  display: "swap",
});

// Configuração da Roboto (Secundária/Leitura)
const roboto = Roboto({ 
  weight: ["400", "500", "700"],
  subsets: ["latin"], 
  variable: "--font-roboto",
  display: "swap",
});

export const metadata: Metadata = {
  title: "InsightFlow",
  description: "Marketing Analytics SaaS",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt" className={`${inter.variable} ${roboto.variable}`}>
      <body className="bg-white text-slate-900 dark:bg-brand-dark dark:text-brand-text antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
