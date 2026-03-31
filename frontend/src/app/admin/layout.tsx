"use client";

import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Aplica tema ao carregar
  useEffect(() => {
    const theme = localStorage.getItem("theme");
    if (theme === "light") {
      document.documentElement.classList.remove("dark");
    } else {
      document.documentElement.classList.add("dark");
    }
  }, []);

  return (
    <div className="flex min-h-screen bg-white text-black dark:bg-slate-950 dark:text-white transition-colors duration-300">
      
      {/* Passamos o estado para a Sidebar saber se deve sumir ou aparecer */}
      <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

      {/* O main agora reage ao estado da sidebar usando margin-left dinâmico */}
      <main 
        className={`
          flex-1 transition-all duration-300 p-8 
          ${sidebarOpen ? "ml-64" : "ml-0"}
        `}
      >
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>

    </div>
  );
}
