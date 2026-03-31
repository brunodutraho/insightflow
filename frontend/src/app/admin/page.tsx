"use client";

import { useEffect, useState, useMemo } from "react";
import api from "@/services/api";
import { useUser } from "@/hooks/useUser";
import { StatCard } from "@/app/admin/components/StatCard";
import { MRRChart } from "@/app/admin/components/MRRChart";
import { SmartIntelligence } from "./components/SmartIntelligence";
import { analyzeSaaSMetrics } from "./lib/analytics";

import { calculateSaaSHealth } from "./lib/healthScore";
import { HealthScoreCard } from "./components/HealthScoreCard";
import { AtRiskClients } from "./components/AtRiskClients";
import { LiveSessionsCard } from "./components/LiveSessionsCard";
import { NewUsersCard } from "./components/NewUsersCard";
import { RecentActivityTimeline } from "./components/RecentActivityTimeline";
import { MRRGoalCard } from "./components/MRRGoalCard";


// --- TIPAGEM DA PÁGINA ---
interface MRRDataPoint { month: string; mrr: number; }

type OverviewData = {
  users: { total: number; new_last_30_days: number; growth_rate: number; };
  companies: { total: number; };
  revenue: { active_subscriptions: number; mrr: number; arpu: number; churn_rate: number; mrr_growth: number; };
  goal: { target: number; expected_progress: number; };
};

interface AtRiskClient {
  id: number;
  name: string;
  last_login_days: number;
  status: string;
}

type ActivityItem = {
  id: string;
  message: string;
  type: "user" | "money" | "alert";
  created_at: string;
};

type AccountActivity = {
  id: string;
  user: string;
  time: string;
};

type SessionActivity = {
  id: string;
  user: string;
  time: string;
  action: string;
};

type DetailedActivity = {
  accounts: AccountActivity[];
  sessions: SessionActivity[];
};

export default function AdminPage() {
  const { user } = useUser();

  const [data, setData] = useState<OverviewData | null>(null);
  const [mrrHistory, setMrrHistory] = useState<MRRDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [atRisk, setAtRisk] = useState<AtRiskClient[]>([]);
  const [activity, setActivity] = useState<ActivityItem[]>([]);
  const [activityData, setActivityData] = useState<DetailedActivity>({
    accounts: [],
    sessions: []
  });

  const health = useMemo(() => calculateSaaSHealth(data), [data]);
  const analysis = useMemo(() => analyzeSaaSMetrics(data), [data]);

  async function fetchData() {
    try {
      const [resOverview, resHistory, resAtRisk, resActivity, resDetailedActivity] = await Promise.all([
        api.get("/admin/overview").catch(() => ({ data: null })),
        api.get("/admin/mrr-history").catch(() => ({ data: [] })),
        api.get("/admin/at-risk-clients").catch(() => ({ data: [] })),
        api.get("/admin/recent-activity").catch(() => ({ data: [] })),
        api.get("/admin/detailed-activity").catch(() => ({
          data: { accounts: [], sessions: [] }
        }))
      ]);

      if (resOverview.data) setData(resOverview.data);
      if (resHistory.data) setMrrHistory(resHistory.data);
      if (resAtRisk.data) setAtRisk(resAtRisk.data);
      if (resActivity.data) setActivity(resActivity.data);
      if (resDetailedActivity.data) setActivityData(resDetailedActivity.data);

    } catch (err) {
      console.error("Erro ao carregar dashboard:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
    
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []); 

  if (loading) return <div className="p-12 text-center animate-pulse italic text-gray-500">Calculando métricas vitais...</div>;
  if (!user || user.role !== "admin") return <div className="p-12 text-red-500 font-bold">Acesso restrito.</div>;


  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-10">
      {/* HEADER */}
      <header>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Dashboard Executivo</h1>
        <p className="text-gray-500">Métricas de Customer Success e Saúde Financeira.</p>
      </header>

      {/* 1. SAÚDE GERAL (PRIORIDADE MÁXIMA) */}
      {/* 1. SAÚDE GERAL E META (PRIORIDADE VISUAL) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <HealthScoreCard health={health} />
          <MRRGoalCard
            current={data?.revenue.mrr ?? 0}
            goal={data?.goal ?? { target: 0, expected_progress: 0 }}
            onUpdate={fetchData} // Sem os parênteses (), passamos a referência da função
          />
      </div>
      
      {/* 2. ATIVIDADE RECENTE + NOVOS USUÁRIOS */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
  
          {/* COLUNA ESQUERDA: NOVOS USUÁRIOS */}
          <NewUsersCard data={activityData.accounts} />

          {/* COLUNA DIREITA: QUEM ESTÁ LOGANDO AGORA */}
          <LiveSessionsCard data={activityData.sessions} />

      </section>
      <RecentActivityTimeline activities={activity} />
      {/* INTELLIGENCE LAYER (ALERTAS + INSIGHTS) */}
      <SmartIntelligence analysis={analysis} />
      <AtRiskClients data={atRisk} />
      {/* MÉTRICAS EM TEMPO REAL (CARDS) */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard label="Total de Usuários" value={data?.users.total} change={data?.users.growth_rate} />
        <StatCard label="Receita Mensal (MRR)" value={data?.revenue.mrr?.toLocaleString('pt-BR')} prefix="R$" change={data?.revenue.mrr_growth} />
        <StatCard label="Taxa de Churn" value={data?.revenue.churn_rate?.toFixed(2)} isPercentage change={data?.revenue.churn_rate && data.revenue.churn_rate > 5 ? -data.revenue.churn_rate : undefined} />
        <StatCard label="Ticket Médio (ARPU)" value={data?.revenue.arpu?.toLocaleString('pt-BR')} prefix="R$" />
        <StatCard label="Assinaturas Ativas" value={data?.revenue.active_subscriptions} />
      </section>

      {/* VISUALIZAÇÃO DE TENDÊNCIA */}
      <section className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-2xl overflow-hidden">
        <MRRChart data={mrrHistory} />
      </section>
    </div>
  );
}
