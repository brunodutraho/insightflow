"use client";

import { useEffect } from "react";
import Sidebar from "./components/Sidebar";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  // aplica tema ao carregar
  useEffect(() => {
    const theme = localStorage.getItem("theme");

    if (theme === "light") {
      document.documentElement.classList.remove("dark");
    } else {
      document.documentElement.classList.add("dark");
    }
  }, []);

  return (
    <div className="flex min-h-screen bg-white text-black dark:bg-slate-950 dark:text-white">

      <Sidebar />

      <main className="flex-1 p-8">
        {children}
      </main>

    </div>
  );
}