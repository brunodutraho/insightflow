"use client";

import { timeAgo } from "../lib/time";

export function NewUsersCard({ data }: { data: any[] }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-2xl shadow-sm h-full">
      <h2 className="text-sm font-bold uppercase tracking-wider text-blue-500 mb-6 flex items-center gap-2">
        <span>🆕</span> Novos Cadastros
      </h2>

      <ul className="space-y-4">
        {data.map((item) => (
          <li key={item.id} className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">
              {item.user?.[0]?.toUpperCase() || "?"}
            </div>

            <div>
              <p className="text-sm font-medium text-slate-700 dark:text-slate-200">
                {item.user}
              </p>

              <p className="text-[10px] text-gray-400 uppercase font-bold">
                Criado {timeAgo(item.time)}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}