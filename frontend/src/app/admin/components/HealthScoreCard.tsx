import { HealthResult } from "../lib/healthScore";

export function HealthScoreCard({ health }: { health: HealthResult }) {
  return (
    <section className={`bg-gradient-to-br ${health.colorClass} text-white p-8 rounded-3xl shadow-lg relative overflow-hidden transition-all duration-500`}>
      {/* Detalhe visual de fundo */}
      <div className="absolute right-[-20px] top-[-20px] w-40 h-40 bg-white/10 rounded-full blur-3xl" />
      
      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-xs uppercase tracking-[0.2em] font-black opacity-80 mb-2">
            Pontuação de Saúde
          </h2>
          <div className="flex items-baseline gap-2">
            <p className="text-6xl font-black tracking-tighter">
              {health.score}
            </p>
            <span className="text-xl opacity-60 font-bold">/100</span>
          </div>
        </div>

        <div className="flex flex-col md:items-end">
          <span className="bg-white/20 backdrop-blur-md px-4 py-1 rounded-full text-sm font-bold mb-2">
            Status: {health.label}
          </span>
          <p className="text-sm opacity-80 text-right max-w-[200px]">
            Índice baseado em retenção, tração de receita e aquisição.
          </p>
        </div>
      </div>
    </section>
  );
}
