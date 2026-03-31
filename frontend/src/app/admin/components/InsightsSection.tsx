interface Insight {
  text: string;
  type: "success" | "danger" | "info" | "warning";
  icon: string;
}

interface InsightsSectionProps {
  insights: Insight[];
}

export function InsightsSection({ insights }: InsightsSectionProps) {
  if (insights.length === 0) return null;

  return (
    <section className="bg-blue-50/50 dark:bg-slate-900/50 border border-blue-100 dark:border-slate-800 p-5 rounded-2xl">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xl">🧠</span>
        <h2 className="text-sm font-bold uppercase tracking-wider text-blue-900 dark:text-blue-400">
          Insights Estratégicos
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {insights.map((insight, index) => (
          <div 
            key={index} 
            className="flex items-center gap-3 p-3 bg-white dark:bg-slate-800 rounded-xl border border-gray-100 dark:border-slate-700 text-sm font-medium shadow-sm transition hover:border-blue-200"
          >
            <span className="text-lg">{insight.icon}</span>
            <span className={insight.type === 'danger' ? 'text-red-600 dark:text-red-400' : 'text-slate-700 dark:text-slate-300'}>
              {insight.text}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
