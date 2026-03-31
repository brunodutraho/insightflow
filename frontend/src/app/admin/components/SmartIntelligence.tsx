// src/app/admin/components/SmartIntelligence.tsx

import { AnalysisResult } from "../lib/analytics";

export function SmartIntelligence({ analysis }: { analysis: AnalysisResult }) {
  const { alerts, insights } = analysis;

  return (
    <div className="space-y-6">
      {/* SEÇÃO DE ALERTAS (VERMELHO) */}
      {alerts.length > 0 && (
        <section className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 p-5 rounded-2xl transition-all">
          <div className="flex items-center gap-2 mb-4">
            <span className="flex h-2 w-2 rounded-full bg-red-500 animate-ping" />
            <h2 className="text-sm font-bold uppercase tracking-widest text-red-800 dark:text-red-400">
              Alertas Críticos
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {alerts.map((alert, i) => (
              <div 
                key={i} 
                className="flex items-center gap-3 p-3 bg-white dark:bg-slate-900 border border-red-100 dark:border-red-900/30 rounded-xl shadow-sm"
              >
                <span className="text-lg">{alert.icon}</span>
                <span className="text-sm font-bold text-red-700 dark:text-red-300">{alert.text}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SEÇÃO DE INSIGHTS (AZUL/DARK) */}
      {insights.length > 0 && (
        <section className="bg-blue-50/50 dark:bg-slate-900/50 border border-blue-100 dark:border-slate-800 p-5 rounded-2xl transition-all">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-lg">🧠</span>
            <h2 className="text-sm font-bold uppercase tracking-widest text-blue-800 dark:text-blue-400">
              Insights Estratégicos
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {insights.map((insight, i) => (
              <div 
                key={i} 
                className="flex items-center gap-3 p-3 bg-white dark:bg-slate-900 border border-gray-100 dark:border-slate-800 rounded-xl shadow-sm"
              >
                <span className="text-lg">{insight.icon}</span>
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{insight.text}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
