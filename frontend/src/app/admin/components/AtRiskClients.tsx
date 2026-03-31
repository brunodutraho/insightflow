"use client";

interface AtRiskClient {
  id: number;
  name: string;
  last_login_days: number;
  status: string; // "inactive" | "payment_issue" | "churn_alert"
}

export function AtRiskClients({ data }: { data: AtRiskClient[] }) {
  // Função auxiliar para renderizar o Badge baseado no status
  const renderStatusBadge = (status: string) => {
    switch (status) {
      case "payment_issue":
        return <span className="px-2 py-0.5 bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 rounded text-[10px] font-bold">PAGAMENTO</span>;
      case "churn_alert":
        return <span className="px-2 py-0.5 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 rounded text-[10px] font-bold">ALERTA CHURN</span>;
      default:
        return <span className="px-2 py-0.5 bg-gray-100 text-gray-600 dark:bg-slate-800 dark:text-slate-400 rounded text-[10px] font-bold">INATIVO</span>;
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 border border-red-100 dark:border-red-900/30 p-6 rounded-2xl shadow-sm h-full">
      <div className="flex items-center gap-2 mb-6">
        <span className="flex h-2 w-2 rounded-full bg-red-500 animate-pulse" />
        <h2 className="text-sm font-bold uppercase tracking-wider text-red-600 dark:text-red-400">
          🚨 Clientes em Risco Imediato
        </h2>
      </div>

      {data.length === 0 ? (
        <p className="text-sm text-gray-500 italic">Nenhum cliente em risco detectado. Ótimo!</p>
      ) : (
        <ul className="space-y-4">
          {data.map((client) => (
            <li
              key={client.id}
              className="flex items-center justify-between p-3 rounded-xl bg-red-50/50 dark:bg-red-950/10 border border-red-100/50 dark:border-red-900/20 transition-all hover:border-red-300 dark:hover:border-red-700"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <p className="font-bold text-slate-800 dark:text-slate-200 text-sm">{client.name}</p>
                  {/* USO DO STATUS AQUI */}
                  {renderStatusBadge(client.status)}
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                  {client.last_login_days} dias sem atividade
                </p>
              </div>

              <button 
                onClick={() => window.location.href = `mailto:?subject=Suporte Prioritário - ${client.name}`}
                className="px-3 py-1.5 bg-white dark:bg-slate-800 border border-red-200 dark:border-red-700 text-[11px] font-bold text-red-600 dark:text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all shadow-sm"
              >
                Resgatar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
