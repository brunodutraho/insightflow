"use client";

import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getDashboard } from "@/services/dashboard.service";

import Overview from "@/components/dashboard/Overview";
import KPIGrid from "@/components/dashboard/KPIGrid";
import InsightsList from "@/components/dashboard/InsightsList";
import SocialCard from "@/components/dashboard/SocialCard";

import { useAuth } from "@/hooks/useAuth";

export default function DashboardPage() {
  const { user } = useAuth(); 
  const [isMounted, setIsMounted] = useState(false);

  const clientId = user?.client_id;

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard", clientId],
    queryFn: () => getDashboard(clientId!),
    enabled: isMounted && !!clientId,
  });

  // 🧠 loading inicial
  if (!isMounted || isLoading || !clientId) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <p className="text-slate-400 animate-pulse">
          Carregando dados do dashboard...
        </p>
      </div>
    );
  }

  // ❌ erro
  if (error || !data) {
    return (
      <div className="p-6 max-w-xl mx-auto mt-10 text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl backdrop-blur">
        <p className="font-semibold">Erro ao carregar dashboard</p>
        <p className="text-sm opacity-70 mt-1">
          Verifique permissões ou tente novamente.
        </p>
      </div>
    );
  }

  // ✅ UI final
  return (
    <div className="space-y-8 animate-in fade-in duration-500 px-4 md:px-8 pb-10">

      {/* HEADER */}
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
          Dashboard
        </h1>
        <p className="text-sm text-slate-400">
          Empresa ID: <span className="text-white font-medium">{clientId}</span>
        </p>
      </header>

      {/* GRID PRINCIPAL */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <Overview overview={data.overview} score={data.score} />
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <SocialCard social={data.social} />
        </div>
      </div>

      {/* KPIs */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <KPIGrid summary={data.kpis.summary} />
      </div>

      {/* INSIGHTS */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <InsightsList insights={data.insights} />
      </div>
    </div>
  );
}