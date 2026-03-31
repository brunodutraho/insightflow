"use client";
export function LiveSessionsCard({ data }: { data: any[] }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-2xl shadow-sm h-full">
      <h2 className="text-sm font-bold uppercase tracking-wider text-amber-500 mb-6 flex items-center gap-2">
        <span className="flex h-2 w-2 rounded-full bg-amber-500 animate-pulse" />
        Sessões Recentes
      </h2>
      <ul className="space-y-4">
        {data.map((item) => (
          <li key={item.id} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <div>
                <p className="text-sm font-medium text-slate-700 dark:text-slate-200">{item.user}</p>
                <p className="text-[10px] text-gray-400 font-bold uppercase">{item.action}</p>
              </div>
            </div>
            <span>
              {new Date(item.time).toLocaleString("pt-BR", {
                timeZone: "America/Sao_Paulo",
                hour: "2-digit",
                minute: "2-digit"
              })}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
