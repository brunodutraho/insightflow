"use client";

import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

// Componente de Tooltip Customizado para suportar Dark Mode e bordas arredondadas
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const currentVal = payload[0].value;
    // Opcional: Se você quiser calcular a variação no futuro, o payload traz os dados do ponto
    
    return (
      <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 p-4 rounded-2xl shadow-xl backdrop-blur-md bg-opacity-90 dark:bg-opacity-90">
        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">{label}</p>
        <div className="flex flex-col gap-1">
          <div className="flex items-center justify-between gap-4">
            <span className="text-sm text-gray-600 dark:text-slate-300">Receita MRR:</span>
            <span className="text-sm font-bold text-emerald-500">
              {Number(currentVal).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </span>
          </div>
          <div className="border-t border-gray-400 dark:border-slate-700 mt-2 pt-2">
            <p className="text-[10px] text-gray-400 leading-tight">
              Métrica baseada em assinaturas ativas no período.
            </p>
          </div>
        </div>
      </div>
    );
  }
  return null;
};

export function MRRChart({ data }: { data: any[] }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Skeleton de carregamento com altura idêntica ao gráfico final
  if (!isMounted) return (
    <div className="h-[400px] w-full bg-slate-50 dark:bg-slate-900/50 animate-pulse rounded-2xl border border-gray-200 dark:border-slate-800" />
  );

  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-2xl shadow-sm">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-lg font-bold text-slate-800 dark:text-white">Evolução do MRR</h2>
          <p className="text-xs text-gray-500 dark:text-slate-400">Desempenho mensal de receita recorrente</p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-50 dark:bg-emerald-500/10 px-3 py-1 rounded-full">
          <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
          <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase">Live</span>
        </div>
      </div>

      {/* 
         O SEGREDO: 
         1. Definimos h-[300px] na div pai (Tailwind)
         2. Definimos height={300} (Número fixo) no ResponsiveContainer
         Isso impede que o Recharts tente adivinhar a altura e falhe com -1.
      */}
      <div className="w-full h-[300px] min-h-[300px]">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data || []} margin={{ top: 5, right: 5, left: -15, bottom: 0 }}>
            <CartesianGrid 
              strokeDasharray="3 3" 
              vertical={false} 
              className="stroke-slate-400 dark:stroke-slate-700"
            />
            
            <XAxis 
              dataKey="month" 
              axisLine={false} 
              tickLine={false} 
              className="fill-slate-100 dark:fill-slate-400 font-semibold"
              tick={{ fontSize: 11 }}
              dy={15}
            />
            
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              className="fill-slate-100 dark:fill-slate-400 font-semibold"
              tick={{ fontSize: 11 }}
              tickFormatter={(val) => `R$${val >= 1000 ? (val/1000).toFixed(0) + 'k' : val}`}
            />

            <Tooltip content={<CustomTooltip />} />
            
            <Line 
              type="monotone" 
              dataKey="mrr" 
              stroke="#10b981" 
              strokeWidth={4} 
              dot={{ r: 5, fill: '#10b981', strokeWidth: 2, stroke: '#fff' }}
              activeDot={{ r: 8, fill: '#10b981', strokeWidth: 3, stroke: '#fff' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

