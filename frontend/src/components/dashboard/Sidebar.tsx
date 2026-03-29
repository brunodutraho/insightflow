"use client";

import { useEffect, useState } from "react"; // Adicione useState e useEffect
import { useUser } from "@/hooks/useUser";
import Link from "next/link";
import { LayoutDashboard, UserPlus, ShieldCheck, Settings } from "lucide-react";

export default function Sidebar() {
  const { user } = useUser();
  const [mounted, setMounted] = useState(false);

  // Garante que o componente só mostre dados do usuário após "hidratar"
  useEffect(() => {
    setMounted(true);
  }, []);

  // Enquanto estiver renderizando no servidor, mostra a versão básica/carregando
  if (!mounted) {
    return <aside className="w-64 bg-slate-900 h-screen p-6 border-r border-slate-800">
      <div className="mb-10 font-bold text-xl text-blue-500">InsightFlow</div>
    </aside>;
  }

  return (
    <aside className="w-64 bg-slate-900 h-screen p-6 border-r border-slate-800">
      <div className="mb-10 font-bold text-xl text-blue-500">InsightFlow</div>
      
      <nav className="space-y-4">
        <Link href="/dashboard" className="block text-slate-300 hover:text-white">Dashboard</Link>

        {/* Agora esta parte só renderiza no Cliente, evitando o erro */}
        {(user?.role === "gestor" || user?.role === "admin") && (
          <div className="pt-4 border-t border-slate-800">
            <p className="text-xs text-slate-500 mb-2">GERENCIAMENTO</p>
            <Link href="/dashboard/users" className="block text-slate-300 hover:text-white">
              Gerar Acesso Cliente
            </Link>
          </div>
        )}
        {user.role === 'admin' && (
        <Link href="/admin" className="flex items-center gap-2 p-2 hover:bg-blue-500/10 rounded-lg text-blue-400">
          <ShieldCheck size={18} />
          CRM Administrativo
        </Link>
        )}
      </nav>
    </aside>
  );
}
