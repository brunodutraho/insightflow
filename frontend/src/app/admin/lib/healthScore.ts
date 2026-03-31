export interface HealthResult {
  score: number;
  label: "Excelente" | "Boa" | "Atenção" | "Crítica" | "N/A";
  colorClass: string;
}

export function calculateSaaSHealth(data: any): HealthResult {
  if (!data) return { score: 0, label: "N/A", colorClass: "from-gray-500 to-gray-600" };

  let score = 0;
  const mrrGrowth = Number(data.revenue?.mrr_growth || 0);
  const churn = Number(data.revenue?.churn_rate || 0);
  const userGrowth = Number(data.users?.growth_rate || 0);

  // 1. MRR Growth (Peso: 40%)
  if (mrrGrowth > 15) score += 40;
  else if (mrrGrowth > 5) score += 30;
  else if (mrrGrowth > 0) score += 20;
  else if (mrrGrowth < 0) score += 5;

  // 2. Churn Rate (Peso: 30%) - Inverso: quanto menor, mais pontos
  if (churn < 2) score += 30;
  else if (churn < 5) score += 20;
  else if (churn < 8) score += 10;
  else score += 0;

  // 3. User Growth (Peso: 30%)
  if (userGrowth > 10) score += 30;
  else if (userGrowth > 0) score += 20;
  else if (userGrowth < 0) score += 5;

  // Classificação e Cores
  if (score >= 85) return { score, label: "Excelente", colorClass: "from-emerald-500 to-teal-600" };
  if (score >= 65) return { score, label: "Boa", colorClass: "from-blue-500 to-indigo-600" };
  if (score >= 45) return { score, label: "Atenção", colorClass: "from-amber-400 to-orange-500" };
  
  return { score, label: "Crítica", colorClass: "from-red-500 to-rose-600" };
}
