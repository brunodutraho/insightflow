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
      
      {/* Sidebar: Ela tem largura fixa (w-64 ou w-20) e empurra o conteúdo naturalmente */}
      <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

      {/* 
          Main: 
          1. flex-1 faz ele ocupar todo o espaço restante.
          2. min-w-0 evita que gráficos ou tabelas quebrem o layout (overflow).
          3. Removidos os ml-0 e mr-1 que causavam o desalinhamento.
      */}
      <main className="flex-1 min-w-0 transition-all duration-300">
        <div className="p-8 max-w-[1600px] mx-auto">
          {children}
        </div>
      </main>

    </div>
  );
}
