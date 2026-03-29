"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const [dark, setDark] = useState(true);

  const menu = [
    { name: "Overview", href: "/admin" },
    { name: "Usuários", href: "/admin/users" },
    { name: "Empresas", href: "/admin/companies" },
  ];

  // 🔥 carregar tema salvo
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
    <aside className="w-64 bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-800 p-6 flex flex-col justify-between">

      {/* TOPO */}
      <div>
        <h2 className="text-xl font-bold mb-8">Admin</h2>

        <nav className="space-y-2">
          {menu.map((item) => {
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  block p-3 rounded-lg transition-all
                  ${isActive
                    ? "bg-gray-200 dark:bg-slate-800 text-black dark:text-white"
                    : "text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-black dark:hover:text-white"}
                `}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* BASE */}
      <div className="space-y-3">

        {/* 🌙 TEMA */}
        <button
          onClick={toggleTheme}
          className="w-full bg-gray-200 dark:bg-slate-800 hover:bg-gray-300 dark:hover:bg-slate-700 p-3 rounded-lg text-sm"
        >
          {dark ? "Modo Claro" : "Modo Escuro"}
        </button>

        {/* 🚪 LOGOUT */}
        <button
          onClick={handleLogout}
          className="w-full bg-red-500/20 hover:bg-red-500/30 text-red-500 p-3 rounded-lg text-sm"
        >
          Sair
        </button>

      </div>
    </aside>
  );
}