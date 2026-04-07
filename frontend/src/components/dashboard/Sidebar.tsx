"use client";

import { useEffect, useState } from "react";
import { useUser } from "@/hooks/useUser";
import Link from "next/link";
import { LayoutDashboard, UserPlus, ShieldCheck, Settings, Users, BarChart3 } from "lucide-react";

export default function Sidebar() {
  const { user } = useUser();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <aside className="w-64 bg-slate-900 h-screen p-6 border-r border-slate-800">
        <div className="mb-10 font-bold text-xl text-blue-500 italic">InsightFlow</div>
      </aside>
    );
  }

  // Atalhos de permissão para facilitar o código
  const isInternalStaff = ["admin_master", "gerente", "suporte", "marketing", "gestor_interno"].includes(user?.role || "");
  const isAdminOrGerente = ["admin_master", "gerente"].includes(user?.role || "");
  const canManageClients = ["admin_master", "gerente", "gestor_assinante", "gestor_interno"].includes(user?.role || "");

  return (
    <aside className="w-64 bg-slate-900 h-screen p-6 border-r border-slate-800 flex flex-col">
      <div className="mb-10 font-bold text-xl text-blue-500 italic">InsightFlow</div>
      
      <nav className="space-y-2 flex-1">
        <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Principal</p>
        
        <Link href="/dashboard" className="flex items-center gap-3 p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </Link>

        {/* ÁREA DE GESTÃO DE CONTAS (Para quem cria acessos) */}
        {canManageClients && (
          <div className="pt-4">
            <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Gestão de Contas</p>
            <Link href="/dashboard/users" className="flex items-center gap-3 p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
              <UserPlus size={18} />
              <span>Criar Acesso Cliente</span>
            </Link>
          </div>
        )}

        {/* ÁREA ADMINISTRATIVA (Master e Gerente apenas) */}
        {isAdminOrGerente && (
          <div className="pt-4">
            <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Plataforma</p>
            <Link href="/admin" className="flex items-center gap-3 p-2 text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all">
              <ShieldCheck size={18} />
              <span className="font-medium">CRM Administrativo</span>
            </Link>
            <Link href="/admin/stats" className="flex items-center gap-3 p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
              <BarChart3 size={18} />
              <span>Métricas Globais</span>
            </Link>
          </div>
        )}
        {isInternalStaff && (
      <div className="pt-4">
        <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Operacional</p>
        <Link href="/dashboard/tickets" className="flex items-center gap-3 p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
          <Users size={18} />
          <span>Tickets Suporte</span>
        </Link>
      </div>
      )}
      </nav>

      {/* RODAPÉ DA SIDEBAR (Configurações) */}
      <div className="pt-4 border-t border-slate-800">
        <Link href="/settings" className="flex items-center gap-3 p-2 text-slate-400 hover:text-white transition-all">
          <Settings size={18} />
          <span>Configurações</span>
        </Link>
      </div>
    </aside>
  );
}
