"use client";

import { MoreHorizontal } from "lucide-react";

interface User {
  id: string;
  email: string;
  role: string;
  status: string;
  tenant_id: string;
  full_name: string | null;
  phone: string | null;
  country: string | null;
  state: string | null;
  company_name: string | null;
  team_size: number | null;
  how_heard: string | null;
  email_verified: boolean;
  terms_accepted: boolean;
  last_login: string | null;
  created_at: string;
  updated_at: string;
}

export function UsersTable({
  users,
  onSelect
}: {
  users: User[];
  onSelect: (user: User) => void;
}) {

  // Tradução e estilização de status para o padrão visual
  const getStatusConfig = (status: string) => {
    switch (status) {
      case "blocked":
        return { label: "Bloqueado", color: "text-rose-500 bg-rose-500/10" };
      case "pending_invite":
        return { label: "Pendente", color: "text-amber-500 bg-amber-500/10" };
      case "inactive":
        return { label: "Inativo", color: "text-slate-500 bg-slate-500/10" };
      default:
        return { label: "Ativo", color: "text-emerald-500 bg-emerald-500/10" };
    }
  };

  // Formatação de data amigável
  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Nunca";
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="text-left text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 dark:border-slate-800">
              <th className="p-5">Usuário / Perfil</th>
              <th>Status</th>
              <th>Empresa</th>
              <th>Último Acesso</th>
              <th className="text-center">E-mail</th>
              <th className="w-10"></th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-50 dark:divide-slate-800/50">
            {users.length === 0 ? (
              <tr>
                <td colSpan={6} className="p-10 text-center text-slate-400 italic">
                  Nenhum usuário encontrado com os filtros selecionados.
                </td>
              </tr>
            ) : (
              users.map((u) => {
                const statusConfig = getStatusConfig(u.status);
                return (
                  <tr
                    key={u.id}
                    className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40 transition-colors group"
                  >
                    <td
                      className="p-5 cursor-pointer"
                      onClick={() => onSelect(u)}
                    >
                      <div className="flex flex-col">
                        <span className="font-bold text-slate-700 dark:text-slate-200">
                          {u.full_name || "Sem Nome"}
                        </span>
                        <span className="text-xs text-slate-400 flex items-center gap-1">
                          {u.email}
                          <span className="text-[10px] bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded text-slate-500 font-medium">
                            {u.role.replace('_', ' ')}
                          </span>
                        </span>
                      </div>
                    </td>

                    <td>
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${statusConfig.color}`}>
                        {statusConfig.label}
                      </span>
                    </td>

                    <td className="text-slate-500 dark:text-slate-400">
                      {u.company_name || "---"}
                    </td>

                    <td className="text-slate-500 dark:text-slate-400">
                      {formatDate(u.last_login)}
                    </td>

                    <td className="text-center">
                      {u.email_verified ? (
                        <span className="text-emerald-500 text-xs font-bold" title="Verificado">✓</span>
                      ) : (
                        <span className="text-slate-300 text-xs font-bold" title="Não Verificado">!</span>
                      )}
                    </td>

                    <td className="p-4">
                      <button
                        onClick={() => onSelect(u)}
                        className="p-2 text-slate-400 hover:text-blue-500 hover:bg-blue-50 dark:hover:bg-slate-800 rounded-xl transition-all"
                      >
                        <MoreHorizontal size={18} />
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
