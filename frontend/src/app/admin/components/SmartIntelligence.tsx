import { AnalysisResult } from "../lib/analytics";

export function SmartIntelligence({ analysis }: { analysis: AnalysisResult }) {
  const { alerts, insights, actions } = analysis;

  return (
    <div className="space-y-6">

      {/* ALERTAS */}
      {alerts.length > 0 && (
        <section className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 p-5 rounded-2xl">
          <h2 className="text-sm font-bold text-red-700 mb-4 uppercase">
            Alertas Críticos
          </h2>

          <div className="space-y-2">
            {alerts.map((a, i) => (
              <div key={i} className="flex gap-3">
                <span>{a.icon}</span>
                <span>{a.text}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* AÇÕES (NOVO - MAIS IMPORTANTE) */}
      {actions.length > 0 && (
        <section className="bg-yellow-50 dark:bg-yellow-900/10 border border-yellow-200 dark:border-yellow-800 p-5 rounded-2xl">
          <h2 className="text-sm font-bold text-yellow-700 mb-4 uppercase">
            Ações Recomendadas
          </h2>

          <div className="space-y-2">
            {actions.map((a, i) => (
              <div key={i} className="flex gap-3">
                <span>{a.icon}</span>
                <span>{a.text}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* INSIGHTS */}
      {insights.length > 0 && (
        <section className="bg-blue-50 dark:bg-slate-900 p-5 rounded-2xl">
          <h2 className="text-sm font-bold text-blue-700 mb-4 uppercase">
            Insights Estratégicos
          </h2>

          <div className="space-y-2">
            {insights.map((i, idx) => (
              <div key={idx} className="flex gap-3">
                <span>{i.icon}</span>
                <span>{i.text}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}