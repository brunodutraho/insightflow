"use client";

import { ActivityItem } from "../page";

interface RecentActivityTimelineProps {
  activities: ActivityItem[];
}

export function RecentActivityTimeline({ activities }: RecentActivityTimelineProps) {
  // ⚡ CORREÇÃO: Os nomes aqui devem ser IGUAIS ao que o Python envia (user, money, alert)
  const stats = {
    assinatura: activities?.filter(a => a.type === 'money').length || 0,
    cadastro: activities?.filter(a => a.type === 'user').length || 0,
    cancelamento: activities?.filter(a => a.type === 'alert').length || 0,
  };

  return (
    <section className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-gray-200 dark:border-slate-800 shadow-sm flex flex-col">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white">
          Linha do Tempo
        </h2>
        
        {/* Filtros/Contadores (Lendo do array do Backend) */}
        <div className="flex gap-2 flex-wrap">
          <div className="flex items-center gap-1.5 bg-emerald-50 dark:bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-100 dark:border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-[11px] font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-tight">
              Assinaturas: {stats.assinatura}
            </span>
          </div>
          <div className="flex items-center gap-1.5 bg-blue-50 dark:bg-blue-500/10 px-3 py-1 rounded-full border border-blue-100 dark:border-blue-500/20">
            <span className="w-2 h-2 rounded-full bg-blue-500"></span>
            <span className="text-[11px] font-bold text-blue-700 dark:text-blue-400 uppercase tracking-tight">
              Cadastros: {stats.cadastro}
            </span>
          </div>
          <div className="flex items-center gap-1.5 bg-rose-50 dark:bg-rose-500/10 px-3 py-1 rounded-full border border-rose-100 dark:border-rose-500/20">
            <span className="w-2 h-2 rounded-full bg-rose-500"></span>
            <span className="text-[11px] font-bold text-rose-700 dark:text-rose-400 uppercase tracking-tight">
              Cancelados: {stats.cancelamento}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-4 max-h-[450px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-200 dark:scrollbar-thumb-slate-800">
        {activities && activities.length > 0 ? (
          activities.map((item) => {
            const date = item?.created_at ? new Date(item.created_at) : null;

            return (
              <div key={item.id} className="flex items-center justify-between border-b border-slate-50 dark:border-slate-800 pb-3 last:border-0 hover:bg-slate-50/50 dark:hover:bg-slate-800/20 transition-colors rounded-lg px-1">
                <div>
                  <p className="text-sm font-medium text-slate-800 dark:text-slate-200">
                    {item.message}
                  </p>
                  <span className={`text-[9px] px-2 py-0.5 rounded font-black uppercase tracking-widest ${
                    item.type === 'money' ? 'bg-emerald-100 text-emerald-700' :
                    item.type === 'user' ? 'bg-blue-100 text-blue-700' :
                    'bg-rose-100 text-rose-700'
                  }`}>
                    {item.type}
                  </span>
                </div>

                <span className="text-xs text-slate-400 font-mono">
                  {date && !isNaN(date.getTime())
                    ? date.toLocaleString("pt-BR", {
                        day: "2-digit",
                        month: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                      })
                    : "--:--"}
                </span>
              </div>
            );
          })
        ) : (
          <div className="py-12 text-center border-2 border-dashed border-slate-100 dark:border-slate-800 rounded-xl">
            <p className="text-sm text-slate-400 italic">Nenhum evento processado.</p>
          </div>
        )}
      </div>
    </section>
  );
}
