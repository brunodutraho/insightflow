"use client";

export function FunnelCard({ data }: { data: any }) {
  if (!data) return null;

  const progress = data.conversion_rate;

  return (
    <div className="bg-white border-opacity-20  dark:bg-slate-900  p-6 rounded-2xl shadow-sm">
      
      <h2 className="text-sm font-bold uppercase text-indigo-500 mb-4">
        🔻 Funil de Conversão (30 dias)
      </h2>

      <div className="space-y-2 text-sm">
        <p>
          👤 Em Experimentação: <b>{data.trials}</b>
        </p>
        <p>
          💰 Assinantes: <b>{data.conversions}</b>
        </p>
      </div>

      {/* BARRA */}
      <div className="mt-4 w-full h-3 bg-gray-200 rounded-lg">
        <div
          className="h-full bg-indigo-500  rounded-lg"
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
      </div>

      <p className="text-xs mt-2 font-bold">
        {progress.toFixed(2)}% de conversão
      </p>

      {/* INSIGHT AUTOMÁTICO */}
      <p className="text-xs mt-2 text-gray-500">
        {progress < 5 && "🚨 Conversão muito baixa — problema no produto ou onboarding"}
        {progress >= 5 && progress < 15 && "⚠️ Conversão ok, mas pode melhorar"}
        {progress >= 15 && "🟢 Conversão saudável"}
      </p>
    </div>
  );
}