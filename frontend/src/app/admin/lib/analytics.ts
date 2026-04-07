export type AnalysisType = "success" | "danger" | "warning" | "info";

export interface DashboardEntry {
  text: string;
  type: AnalysisType;
  icon: string;
}

export interface ActionItem {
  text: string;
  icon: string;
  priority: "high" | "medium" | "low";
}

export interface AnalysisResult {
  alerts: DashboardEntry[];
  insights: DashboardEntry[];
  actions: ActionItem[];
}

export function analyzeSaaSMetrics(data: any): AnalysisResult {
  const alerts: DashboardEntry[] = [];
  const insights: DashboardEntry[] = [];
  const actions: ActionItem[] = [];

  if (!data) return { alerts, insights, actions };

  const mrrGrowth = Number(data.revenue?.mrr_growth || 0);
  const churn = Number(data.revenue?.churn_rate || 0);
  const userGrowth = Number(data.users?.growth_rate || 0);
  const arpu = Number(data.revenue?.arpu || 0);
  const mrr = Number(data.revenue?.mrr || 0);

  // =========================
  // ALERTAS
  // =========================
  if (mrrGrowth < 0) {
    alerts.push({
      text: "MRR em queda nos últimos 30 dias",
      type: "danger",
      icon: "🚨",
    });

    actions.push({
      text: "Revisar estratégia de aquisição imediatamente",
      icon: "🎯",
      priority: "high",
    });
  }

  if (churn > 8) {
    alerts.push({
      text: "Churn crítico (>8%)",
      type: "danger",
      icon: "🛑",
    });

    actions.push({
      text: "Entrar em contato com clientes em risco HOJE",
      icon: "📞",
      priority: "high",
    });
  } else if (churn > 5) {
    alerts.push({
      text: "Churn acima da média",
      type: "warning",
      icon: "⚠️",
    });

    actions.push({
      text: "Analisar feedbacks e motivos de cancelamento",
      icon: "🧠",
      priority: "medium",
    });
  }

  if (userGrowth < 0) {
    alerts.push({
      text: "Queda na base de usuários",
      type: "danger",
      icon: "📉",
    });

    actions.push({
      text: "Reativar campanhas de aquisição",
      icon: "🚀",
      priority: "high",
    });
  }

  // =========================
  // INSIGHTS
  // =========================
  if (mrrGrowth > 10) {
    insights.push({
      text: "Crescimento acelerado de receita",
      type: "success",
      icon: "🚀",
    });
  }

  if (userGrowth > 15) {
    insights.push({
      text: "Alta aquisição de usuários",
      type: "success",
      icon: "📈",
    });
  }

  if (arpu < 50 && arpu > 0) {
    insights.push({
      text: "ARPU baixo → oportunidade de upsell",
      type: "info",
      icon: "💡",
    });

    actions.push({
      text: "Criar plano premium ou upgrade",
      icon: "💰",
      priority: "medium",
    });
  }

  if (mrr === 0) {
    actions.push({
      text: "Ativar monetização (nenhuma receita ainda)",
      icon: "🔥",
      priority: "high",
    });
  }

  // fallback
  if (alerts.length === 0 && insights.length === 0) {
    insights.push({
      text: "Operação estável",
      type: "info",
      icon: "📊",
    });
  }

  return { alerts, insights, actions };
}