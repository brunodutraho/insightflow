"use client";

import { timeAgo } from "../lib/time";

export function LiveSessionsCard({ data }: { data: any[] }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-2xl shadow-sm h-full">
      <h2 className="text-sm font-bold uppercase tracking-wider text-green-500 mb-6 flex items-center gap-2">
        <span>🟢</span> Sessões Ativas
      </h2>

      <ul className="space-y-4">
        {data.map((item) => (
          <li key={item.id} className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-700 dark:text-slate-200">
                {item.user}
              </p>

              <p className="text-[10px] text-gray-400 uppercase font-bold">
                {item.action} • {timeAgo(item.time)}
              </p>
            </div>

            <span className="text-[10px] bg-green-100 text-green-600 px-2 py-0.5 rounded font-bold">
              online
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}