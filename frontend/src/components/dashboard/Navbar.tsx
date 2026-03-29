"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Cookies from "js-cookie";
import Link from "next/link";
import ClientSelector from "./ClientSelector";
import { useUser } from "@/hooks/useUser";

export default function Navbar() {
  const { user } = useUser();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleLogout = () => {
    Cookies.remove("token");
    localStorage.removeItem("token");
    router.push("/login");
  };

  // Enquanto não monta, renderiza um esqueleto ou barra simples para evitar erro
  if (!mounted) return <nav className="h-[73px] bg-slate-900 border-b border-slate-800" />;

  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-slate-900 border-b border-slate-800 shadow-xl text-white">
      <div className="flex items-center gap-6">
        <Link href="/dashboard" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent font-sans">
          InsightFlow
        </Link>
        <ClientSelector />
      </div>

      <div className="flex items-center gap-4">
        <div className="flex flex-col items-end mr-2 font-sans">
          <span className="text-sm font-semibold">ID: {user.id}</span>
          <span className="text-[10px] uppercase tracking-widest text-blue-500 font-bold">
            {user.role}
          </span>
        </div>
        <button onClick={handleLogout} className="..."> Sair </button>
      </div>
    </nav>
  );
}
