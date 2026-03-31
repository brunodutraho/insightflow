// src/app/admin/components/NewUsersCard.tsx
"use client";

import React from "react";

interface AccountActivity {
  id: string;
  user: string;
  time: string;
}

interface NewUsersCardProps {
  data: AccountActivity[];
}

export function NewUsersCard({ data }: NewUsersCardProps) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-2xl shadow-sm h-full">
      <h2 className="text-sm font-bold uppercase tracking-wider text-blue-500 mb-6 flex items-center gap-2">
        <span>🆕</span> Novos Cadastros
      </h2>

      {data && data.length > 0 ? (
        <ul className="space-y-4">
          {data.map((item) => {
            // O backend envia "time" no formato ISO
            const rawDate = item.time;
            const date = rawDate ? new Date(rawDate) : null;

            return (
              <li key={item.id} className="flex items-center gap-3">
                {/* Avatar circular com a primeira letra */}
                <div className="w-8 h-8 flex-shrink-0 bg-blue-50 dark:bg-blue-900/20 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold border border-blue-100 dark:border-blue-800">
                  {item.user?.[0]?.toUpperCase() || "?"}
                </div>

                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate">
                    {item.user}
                  </p>

                  <p className="text-[10px] text-gray-400 uppercase font-bold tracking-tight">
                    Criado em{" "}
                    <span className="text-slate-500 dark:text-slate-400">
                      {date && !isNaN(date.getTime())
                        ? date.toLocaleString("pt-BR", {
                            timeZone: "America/Sao_Paulo",
                            day: "2-digit",
                            month: "2-digit",
                            hour: "2-digit",
                            minute: "2-digit",
                          })
                        : "--:--"}
                    </span>
                  </p>
                </div>
              </li>
            );
          })}
        </ul>
      ) : (
        <div className="h-full flex items-center justify-center py-10">
          <p className="text-xs text-slate-400 italic font-medium">Nenhum cadastro recente.</p>
        </div>
      )}
    </div>
  );
}
