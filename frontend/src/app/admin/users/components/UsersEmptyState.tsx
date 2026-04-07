import { SearchX } from "lucide-react";

export function UsersEmptyState() {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-20 text-center flex flex-col items-center shadow-sm">
      <div className="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mb-6 text-slate-400">
        <SearchX size={32} />
      </div>
      
      <p className="text-lg font-bold text-slate-700 dark:text-slate-200">
        Nenhum usuário encontrado
      </p>
      <p className="text-sm text-slate-400 mt-2 max-w-xs mx-auto">
        Não encontramos resultados para os filtros selecionados. Tente buscar outro termo ou limpar os filtros.
      </p>
    </div>
  );
}
