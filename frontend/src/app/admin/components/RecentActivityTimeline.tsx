import { timeAgo } from "../lib/time";

type Priority = "high" | "medium" | "low";

const priorityStyles: Record<Priority, string> = {
  high: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  medium: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  low: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
};

export function RecentActivityTimeline({ activities }: { activities: any[] }) {
  return (
    <section className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-gray-200 dark:border-slate-800 shadow-sm">
      <h2 className="text-lg font-bold mb-6 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
        Atividade Recente
      </h2>

      <div className="space-y-6 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
        {activities?.map((item) => (
          <div key={item.id} className="relative pl-6 border-l-2 border-slate-100 dark:border-slate-800 pb-1 last:border-transparent">
            {/* Dot indicador na linha do tempo */}
            <div className="absolute -left-[9px] top-1 w-4 h-4 rounded-full border-4 border-white dark:border-slate-900 bg-slate-300 dark:bg-slate-700" />
            
            <div className="flex justify-between items-start gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-200">{item.message}</p>
                <div className="flex gap-2 mt-1.5">
                  <span className="text-[10px] bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded uppercase font-bold text-slate-500">
                    {item.type}
                  </span>
                  <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${priorityStyles[item.priority as Priority || "low"]}`}>
                    {item.priority || "low"}
                  </span>
                </div>
              </div>
              <time className="text-[11px] font-medium text-slate-400 whitespace-nowrap">
                {timeAgo(item.created_at)}
              </time>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
