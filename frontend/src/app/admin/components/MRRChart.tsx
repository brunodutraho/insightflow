"use client";

import { useEffect, useState, useRef } from "react";
import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Area,
} from "recharts";

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const real = payload.find((p: any) => p.dataKey === "mrr")?.value || 0;
    const meta = payload.find((p: any) => p.dataKey === "goal")?.value || 0;
    const met = real >= meta;

    return (
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl shadow-2xl min-w-[200px]">
        <p className="text-[10px] font-black text-slate-400 uppercase mb-3 tracking-widest">{label}</p>
        <div className="space-y-2">
          <div className="flex justify-between gap-4">
            <span className="text-[10px] font-bold text-slate-500 uppercase">Faturamento:</span>
            <span className="text-sm font-black text-emerald-500">{real.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}</span>
          </div>
          <div className="flex justify-between gap-4 border-t pt-2">
            <span className="text-[10px] font-bold text-slate-500 uppercase">Meta:</span>
            <span className="text-sm font-bold text-purple-500">{meta.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}</span>
          </div>
          <div className={`mt-2 py-1 text-center rounded text-[10px] font-bold ${met ? "bg-emerald-100 text-emerald-700" : "bg-rose-100 text-rose-700"}`}>
            {met ? "🚀 Meta batida" : `⚠️ Faltam R$ ${(meta - real).toLocaleString("pt-BR")}`}
          </div>
        </div>
      </div>
    );
  }
  return null;
};

export function MRRChart({ data }: { data: any[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 300 });

  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        const { width } = entry.contentRect;
        if (width > 0) {
          setDimensions({ width, height: 300 });
        }
      }
    });

    resizeObserver.observe(containerRef.current);
    return () => resizeObserver.disconnect();
  }, []);

  return (
    <div className="w-full min-h-[420px] bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-3xl shadow-sm">
      <div className="mb-6">
        <h2 className="text-lg font-black text-slate-800 dark:text-white uppercase italic">Evolução de Performance</h2>
        <p className="text-xs text-slate-400">Faturamento vs Meta</p>
      </div>

      <div ref={containerRef} className="w-full h-[300px] flex items-center justify-center">
        {dimensions.width > 0 ? (
          <ComposedChart
            width={dimensions.width}
            height={dimensions.height}
            data={data?.length > 0 ? data : [{ month: "-", mrr: 0, goal: 0 }]}
            margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorMrr" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" opacity={0.5} />
            <XAxis dataKey="month" tick={{ fontSize: 10, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <YAxis hide domain={['auto', 'auto']} />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#8b5cf6', strokeWidth: 1 }} />
            <Line type="stepAfter" dataKey="goal" stroke="#a855f7" strokeDasharray="6 4" dot={false} strokeWidth={2} />
            <Area type="monotone" dataKey="mrr" stroke="#8b5cf6" fill="url(#colorMrr)" strokeWidth={3} />
          </ComposedChart>
        ) : (
          <div className="w-full h-full animate-pulse bg-slate-100 dark:bg-slate-800 rounded-xl" />
        )}
      </div>
    </div>
  );
}
