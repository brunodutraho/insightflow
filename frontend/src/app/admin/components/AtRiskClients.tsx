"use client";

import { useRouter } from "next/navigation";

interface AtRiskClient {
  id: number;
  name: string;
  last_login_days: number;
  status: string;
}

export function AtRiskClients({ data }: { data: AtRiskClient[] }) {
  const router = useRouter();

  // 🔥 Ordena por risco (mais dias offline primeiro)
  const sortedData = [...data].sort(
    (a, b) => b.last_login_days - a.last_login_days
  );

  const getRiskLevel = (days: number) => {
    if (days >= 15) return "critical";
    if (days >= 7) return "warning";
    return "low";
  };

  const renderStatusBadge = (client: AtRiskClient) => {
    const level = getRiskLevel(client.last_login_days);

    switch (level) {
      case "critical":
        return (
          <span className="px-2 py-0.5 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 rounded text-[10px] font-bold uppercase">
            Crítico
          </span>
        );
      case "warning":
        return (
          <span className="px-2 py-0.5 bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 rounded text-[10px] font-bold uppercase">
            Atenção
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 bg-gray-100 text-gray-600 dark:bg-slate-800 dark:text-slate-400 rounded text-[10px] font-bold uppercase">
            Inativo
          </span>
        );
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 border border-red-100 dark:border-red-900/30 p-6 rounded-2xl shadow-sm h-full flex flex-col">
      
      {/* HEADER */}
      <div className="flex items-center justify-between mb-6 shrink-0">
        <div className="flex items-center gap-2">
          <span className="flex h-2 w-2 rounded-full bg-red-500 animate-pulse" />
          <h2 className="text-sm font-black uppercase tracking-widest text-red-600 dark:text-red-400">
            🚨 Clientes em Risco
          </h2>
        </div>
        <span className="text-[10px] font-bold text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded-full">
          {sortedData.length} alertas
        </span>
      </div>

      {/* EMPTY STATE */}
      {sortedData.length === 0 ? (
        <div className="flex-1 flex items-center justify-center border-2 border-dashed border-slate-50 dark:border-slate-800 rounded-2xl p-8">
          <p className="text-sm text-gray-400 italic font-medium text-center">
            Nenhum cliente em risco identificado.
          </p>
        </div>
      ) : (
        <>
          <ul className="space-y-3 overflow-y-auto max-h-[380px] pr-2 flex-1 custom-scrollbar">
            {sortedData.map((client) => {
              const risk = getRiskLevel(client.last_login_days);

              return (
                <li
                  key={client.id}
                  className={`flex items-center justify-between p-3 rounded-xl border transition-all
                    ${
                      risk === "critical"
                        ? "bg-red-50/40 dark:bg-red-950/20 border-red-200 dark:border-red-900/40"
                        : risk === "warning"
                        ? "bg-amber-50/40 dark:bg-amber-950/20 border-amber-200 dark:border-amber-900/40"
                        : "bg-slate-50 dark:bg-slate-800/40 border-slate-200 dark:border-slate-700"
                    }
                  `}
                >
                  {/* INFO */}
                  <div className="min-w-0 flex-1 mr-3">
                    <div className="flex items-center gap-2 flex-wrap">
                      <p className="font-bold text-slate-800 dark:text-slate-200 text-sm truncate">
                        {client.name}
                      </p>
                      {renderStatusBadge(client)}
                    </div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
                      {client.last_login_days} dias sem atividade
                    </p>
                  </div>

                  {/* ACTION INDIVIDUAL (Opcional, mantido para agilidade) */}
                  <button
                    onClick={() => router.push(`/admin/users?id=${client.id}`)}
                    className="shrink-0 p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
                    title="Ver Detalhes"
                  >
                    <svg xmlns="http://w3.org" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                  </button>
                </li>
              );
            })}
          </ul>

          {/* BOTÃO GERENCIAR TODOS (Ação Centralizada) */}
          <button
            onClick={() => router.push("/admin/users?filter=at_risk")}
            className="w-full mt-4 px-4 py-3 bg-red-600 hover:bg-red-700 text-white text-[11px] font-black rounded-xl transition-all uppercase tracking-widest shadow-lg shadow-red-500/20"
          >
            Gerenciar Todos os Riscos
          </button>
        </>
      )}
    </div>
  );
}
