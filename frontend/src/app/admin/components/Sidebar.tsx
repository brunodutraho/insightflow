"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";
import { Menu, X, Sun, Moon, LogOut } from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export default function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();

  const [dark, setDark] = useState(true);

  const menu = [
    { name: "Overview", href: "/admin", icon: "📊" },
    { name: "Usuários", href: "/admin/users", icon: "👥" },
    { name: "Empresas", href: "/admin/companies", icon: "🏢" },
    { name: "Planos", href: "/admin/plans", icon: "💳" },
    { name: "Cupons", href: "/admin/coupons", icon: "🎟️" },
  ];

  // Carregar tema salvo
  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "light") {
      setDark(false);
      document.documentElement.classList.remove("dark");
    } else {
      setDark(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  function toggleTheme() {
    const newTheme = !dark;
    setDark(newTheme);
    if (newTheme) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }

  function handleLogout() {
    localStorage.removeItem("token");
    Cookies.remove("token");
    router.push("/login");
  }

  return (
    <>
      {/* BOTÃO PARA ABRIR (Aparece fixo quando a sidebar some) */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed top-6 left-6 z-50 p-2.5 bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl shadow-lg hover:scale-110 transition-all text-blue-600"
        >
          <Menu size={20} />
        </button>
      )}

      {/* SIDEBAR FIXA */}
      <aside
        className={`
          fixed top-0 left-0 h-screen z-40
          bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-800 
          transition-all duration-300 ease-in-out flex flex-col justify-between
          ${isOpen ? "w-64 p-6 translate-x-0" : "w-0 -translate-x-full p-0"}
        `}
      >
        {/* CONTEÚDO DA SIDEBAR (Esconde o conteúdo interno para não "esmagar" na animação) */}
        <div className={`${isOpen ? "opacity-100 delay-100" : "opacity-0"} transition-all duration-200`}>
          
          {/* TOPO */}
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-500 bg-clip-text text-transparent">
              Painel Admin
            </h2>
            <button 
              onClick={() => setIsOpen(false)}
              className="p-1.5 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg text-gray-400 transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          {/* MENU */}
          <nav className="space-y-1.5">
            {menu.map((item) => {
              const isActive =
                pathname === item.href || pathname.startsWith(item.href + "/");

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`
                    flex items-center gap-3 p-3 rounded-xl transition-all font-medium
                    ${isActive
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20"
                      : "text-gray-500 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-black dark:hover:text-white"}
                  `}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* BASE (BOTÕES INFERIORES) */}
        <div className={`space-y-3 ${isOpen ? "opacity-100 delay-100" : "opacity-0"} transition-all duration-200`}>
          
          {/* MODO DARK/LIGHT */}
          <button
            onClick={toggleTheme}
            className="w-full flex items-center justify-center gap-2 bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 p-3 rounded-xl text-sm font-semibold transition-colors"
          >
            {dark ? <Sun size={16} /> : <Moon size={16} />}
            {dark ? "Modo Claro" : "Modo Escuro"}
          </button>

          {/* LOGOUT */}
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 bg-red-500/10 hover:bg-red-500 text-red-600 hover:text-white p-3 rounded-xl text-sm font-bold transition-all"
          >
            <LogOut size={16} />
            Sair
          </button>

        </div>
      </aside>
    </>
  );
}
