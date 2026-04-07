"use client";

import { useEffect, useState, useMemo } from "react";
import api from "@/services/api";
import { useUser } from "@/hooks/useUser";

// COMPONENTES
import { StatCard } from "@/app/admin/components/StatCard";
import { MRRChart } from "@/app/admin/components/MRRChart";
import { SmartIntelligence } from "./components/SmartIntelligence";
import { HealthScoreCard } from "./components/HealthScoreCard";
import { AtRiskClients } from "./components/AtRiskClients";
import { LiveSessionsCard } from "./components/LiveSessionsCard";
import { NewUsersCard } from "./components/NewUsersCard";
import { RecentActivityTimeline } from "./components/RecentActivityTimeline";
import { MRRGoalCard } from "./components/MRRGoalCard";
import { FunnelCard } from "./components/FunnelCard";

// LÓGICA
import { analyzeSaaSMetrics } from "./lib/analytics";
import { calculateSaaSHealth } from "./lib/healthScore";

// --- TIPAGENS ---
interface MRRDataPoint {
  month: string;
  mrr: number;
}

type OverviewData = {
  users: {
    total: number;
    new_last_30_days: number;
    growth_rate: number;
  };
  companies: {
    total: number;
  };
  revenue: {
    active_subscriptions: number;
    mrr: number;
    arpu: number;
    churn_rate: number;
    mrr_growth: number;
  };
  goal: {
    target: number;
    expected_progress: number;
  };
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
  priority?: "high" | "medium" | "low";
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

type FunnelData = {
  trials: number;
  conversions: number;
  conversion_rate: number;
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
    sessions: [],
  });
  const [funnel, setFunnel] = useState<FunnelData | null>(null);

  // 🔥 INTELIGÊNCIA
  const health = useMemo(() => calculateSaaSHealth(data), [data]);
  const analysis = useMemo(() => analyzeSaaSMetrics(data), [data]);

  // 🔄 FETCH CENTRAL
    // 🔄 FETCH CENTRAL
  async function fetchData() {
    try {
      // 🔥 Cache Buster: Adiciona um timestamp único para cada requisição.
      // Isso força o navegador e o Next.js a buscarem o dado real do banco.
      const ts = `?t=${Date.now()}`;

      const [
        resOverview,
        resHistory,
        resAtRisk,
        resActivity,
        resDetailedActivity,
        resFunnel,
      ] = await Promise.all([
        api.get(`/admin/overview${ts}`).catch(() => ({ data: null })),
        api.get(`/admin/mrr-history${ts}`).catch(() => ({ data: [] })),
        api.get(`/admin/at-risk-clients${ts}`).catch(() => ({ data: [] })),
        api.get(`/admin/recent-activity${ts}`).catch(() => ({ data: [] })),
        api.get(`/admin/detailed-activity${ts}`).catch(() => ({
          data: { accounts: [], sessions: [] },
        })),
        api.get(`/admin/funnel${ts}`).catch(() => ({ data: null })),
        api.get(`/admin/insights${ts}`).catch(() => ({ data: [] })),
      ]);

      // Atribuição reativa: O React detecta a mudança no objeto 'data' e 
      // propaga para o MRRGoalCard e para o HealthScoreCard via useMemo.
      if (resOverview.data) setData(resOverview.data);
      
      // Essencial: Se a meta mudou, o histórico (MRRChart) precisa ser atualizado 
      // pois a linha de 'goal' do gráfico vem daqui.
      if (resHistory.data) setMrrHistory(resHistory.data);
      
      if (resAtRisk.data) setAtRisk(resAtRisk.data);
      if (resActivity.data) setActivity(resActivity.data);
      if (resDetailedActivity.data) setActivityData(resDetailedActivity.data);
      if (resFunnel.data) setFunnel(resFunnel.data);

      console.log("✅ Dashboard sincronizado com o banco de dados.");
    } catch (err) {
      console.error("❌ Erro crítico ao carregar dashboard:", err);
    } finally {
      setLoading(false);
    }
  }


  // 🔄 AUTO REFRESH
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  if (loading)
    return (
      <div className="p-12 text-center animate-pulse italic text-gray-500">
        Calculando métricas vitais...
      </div>
    );

  if (!user || user.role !== "admin_master")
    return (
      <div className="p-12 text-red-500 font-bold">
        Acesso restrito.
      </div>
    );

  return (
    <div className="space-y-10 max-w-7xl mx-auto pb-10">

      {/* HEADER */}
      <header>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          Dashboard Executivo
        </h1>
        <p className="text-gray-500">
          Métricas de Customer Success e Saúde Financeira.
        </p>
      </header>

      {/* ========================= */}
      {/* 1. SAÚDE + META */}
      {/* ========================= */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <HealthScoreCard health={health} />

        <MRRGoalCard
          current={data?.revenue.mrr ?? 0}
          goal={data?.goal ?? { target: 0, expected_progress: 0 }}
          onUpdate={fetchData}
        />
      </div>

      {/* ========================= */}
      {/* 2. FUNIL (CRESCIMENTO) */}
      {/* ========================= */}
      <FunnelCard data={funnel} />

      {/* ========================= */}
      {/* 3. ATIVIDADE AO VIVO */}
      {/* ========================= */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <NewUsersCard data={activityData.accounts} />
        <LiveSessionsCard data={activityData.sessions} />
      </section>

      {/* ========================= */}
      {/* 4. INSIGHTS INTELIGENTES */}
      {/* ========================= */}
      <SmartIntelligence analysis={analysis} />

      {/* ========================= */}
      {/* 5. RISCO (CHURN) */}
      {/* ========================= */}
      <AtRiskClients data={atRisk} />

      {/* ========================= */}
      {/* 6. TIMELINE */}
      {/* ========================= */}
      <RecentActivityTimeline activities={activity} />

      {/* ========================= */}
      {/* 7. MÉTRICAS CORE */}
      {/* ========================= */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          label="Total de Usuários"
          value={data?.users.total}
          change={data?.users.growth_rate}
        />

        
        <StatCard
          label="Assinaturas Ativas"
          value={data?.revenue.active_subscriptions}
        />

        <StatCard
          label="Taxa de Cancelamento"
          value={data?.revenue.churn_rate?.toFixed(2)}
          isPercentage
        />

      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        <StatCard
          label="Receita Mensal (MRR)"
          value={data?.revenue.mrr?.toLocaleString("pt-BR")}
          prefix="R$"
          change={data?.revenue.mrr_growth}
        />

        <StatCard
            label="Receita Média por Usuário (ARPU)"
            value={data?.revenue.arpu?.toLocaleString("pt-BR")}
            prefix="R$"
          />

      </section>

      {/* ========================= */}
      {/* 8. TENDÊNCIA */}
      {/* ========================= */}
      <section className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-2xl overflow-hidden min-h-[420px]">
        <MRRChart data={mrrHistory} />
      </section>

    </div>
  );
}