"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";
import { 
  Sun, Moon, LogOut, 
  LayoutDashboard, Users, Building2, 
  CreditCard, Ticket, Globe, 
  ChevronLeft, ChevronRight 
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export default function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [dark, setDark] = useState(true);

  const menu = [
    { name: "Overview", href: "/admin", icon: LayoutDashboard, exact: true },
    { name: "Usuários", href: "/admin/users", icon: Users },
    { name: "Empresas", href: "/admin/companies", icon: Building2 },
    { name: "Planos", href: "/admin/plans", icon: CreditCard },
    { name: "Cupons", href: "/admin/coupons", icon: Ticket },
  ];

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    const isLight = saved === "light";
    setDark(!isLight);
    document.documentElement.classList.toggle("dark", !isLight);
  }, []);

  function toggleTheme() {
    const newTheme = !dark;
    setDark(newTheme);
    document.documentElement.classList.toggle("dark", newTheme);
    localStorage.setItem("theme", newTheme ? "dark" : "light");
  }

  function handleLogout() {
    localStorage.removeItem("token");
    Cookies.remove("token");
    router.push("/login");
  }

  return (
    <aside
      className={`
        sticky top-0 h-screen z-40
        bg-white dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800/50 
        transition-all duration-300 ease-in-out flex flex-col
        ${isOpen ? "w-64" : "w-20"}
      `}
    >
      {/* HEADER: LOGO + BOTÃO FIXO */}
      <div className="p-4 flex flex-col items-center gap-4 shrink-0">
        <div className={`flex items-center gap-3 w-full ${isOpen ? "justify-start px-2" : "justify-center"}`}>
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30 text-white shrink-0">
            <Globe size={22} />
          </div>
          {isOpen && (
            <h2 className="text-lg font-black tracking-tighter text-slate-900 dark:text-white truncate animate-in fade-in duration-300">
              Insight<span className="text-blue-600">Flow</span>
            </h2>
          )}
        </div>

        <button 
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-center p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg text-slate-400 border border-transparent hover:border-slate-200 dark:hover:border-slate-700 transition-all"
        >
          {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} className="text-blue-600" />}
        </button>
      </div>

      {/* NAVEGAÇÃO COM EFEITO DE ENTRADA/SAÍDA */}
      <nav className="flex-1 px-3 space-y-1 relative overflow-y-auto custom-scrollbar overflow-x-hidden pt-4">
        {menu.map((item) => {
          const isActive = item.exact 
            ? pathname === item.href 
            : pathname.startsWith(item.href) && pathname !== "/admin";

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`
                group relative flex items-center p-3 rounded-xl transition-all duration-500 font-semibold text-sm
                ${isOpen ? "justify-start gap-3" : "justify-center"}
                ${isActive ? "text-white" : "text-slate-500 dark:text-slate-400 hover:text-blue-600"}
              `}
            >
              {/* BACKGROUND ANIMADO (ENTRADA E SAÍDA) */}
              <div 
                className={`
                  absolute inset-0 bg-blue-600 rounded-xl shadow-lg shadow-blue-600/30 z-0
                  transition-all duration-300 ease-in-out
                  ${isActive 
                    ? "opacity-100 scale-100 visible animate-in fade-in zoom-in-95" 
                    : "opacity-0 scale-90 invisible"
                  }
                `}
              />

              {/* CONTEÚDO */}
              <div className={`relative z-10 flex items-center gap-3 w-full ${!isOpen && 'justify-center'}`}>
                <item.icon 
                   size={22} 
                   className={`transition-all duration-300 ${isActive ? "text-white scale-110" : "group-hover:scale-110 group-hover:text-blue-600"}`} 
                />
                {isOpen && (
                  <span className="truncate transition-all duration-300">
                    {item.name}
                  </span>
                )}
                {isOpen && isActive && (
                  <div className="ml-auto w-1 h-5 bg-white rounded-full animate-pulse" />
                )}
              </div>
            </Link>
          );
        })}
      </nav>

      {/* FOOTER */}
      <div className="p-3 border-t border-slate-100 dark:border-slate-800 space-y-2 shrink-0">
        <button
          onClick={toggleTheme}
          className={`flex items-center justify-center bg-slate-50 dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-all border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300
            ${isOpen ? "w-full gap-3 p-2.5" : "w-full p-2.5"}`}
        >
          {dark ? <Sun size={18} className="text-amber-500" /> : <Moon size={18} className="text-blue-600" />}
          {isOpen && <span className="text-[10px] font-black uppercase tracking-wider">Mudar Tema</span>}
        </button>

        <button
          onClick={handleLogout}
          className={`flex items-center justify-center rounded-xl font-bold text-rose-500 hover:bg-rose-500/10 hover:text-rose-600 dark:hover:bg-rose-500/20 transition-all duration-300
            ${isOpen ? "w-full gap-3 p-2.5" : "w-full p-2.5"}`}
        >
          <LogOut size={20} />
          {isOpen && <span className="text-xs">Sair</span>}
        </button>
      </div>
    </aside>
  );
}
