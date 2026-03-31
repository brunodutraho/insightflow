// src/app/admin/lib/analytics.ts

export type AnalysisType = "success" | "danger" | "warning" | "info";

export interface DashboardEntry {
  text: string;
  type: AnalysisType;
  icon: string;
}

export interface AnalysisResult {
  alerts: DashboardEntry[];
  insights: DashboardEntry[];
}

export function analyzeSaaSMetrics(data: any): AnalysisResult {
  const alerts: DashboardEntry[] = [];
  const insights: DashboardEntry[] = [];

  if (!data) return { alerts, insights };

  const mrrGrowth = Number(data.revenue?.mrr_growth || 0);
  const churn = Number(data.revenue?.churn_rate || 0);
  const userGrowth = Number(data.users?.growth_rate || 0);
  const arpu = Number(data.revenue?.arpu || 0);

  // --- ENGINE DE ALERTAS (Críticos/Ação Imediata) ---
  if (mrrGrowth < 0) {
    alerts.push({ text: "Receita Mensal (MRR) em queda nos últimos 30 dias", type: "danger", icon: "🚨" });
  }
  
  if (churn > 8) {
    alerts.push({ text: "Churn Crítico (>8%): Risco imediato de insolvência", type: "danger", icon: "🛑" });
  } else if (churn > 5) {
    alerts.push({ text: "Churn acima da média: Verifique a satisfação do cliente", type: "warning", icon: "⚠️" });
  }

  if (userGrowth < 0) {
    alerts.push({ text: "Queda real na base de usuários ativos", type: "danger", icon: "📉" });
  }

  // --- ENGINE DE INSIGHTS (Oportunidades/Sucesso) ---
  if (mrrGrowth > 10) {
    insights.push({ text: "Crescimento de receita acelerado (+10%)", type: "success", icon: "🚀" });
  }

  if (userGrowth > 15) {
    insights.push({ text: "Viralidade detectada: Alto volume de novos usuários", type: "success", icon: "📈" });
  }

  if (arpu < 50 && arpu > 0) {
    insights.push({ text: "Ticket médio baixo: Oportunidade para estratégias de Upsell", type: "info", icon: "💡" });
  }

  // Caso esteja tudo estável
  if (alerts.length === 0 && insights.length === 0) {
    insights.push({ text: "Operação estável. Nenhuma anomalia detectada.", type: "info", icon: "📊" });
  }

  return { alerts, insights };
}
