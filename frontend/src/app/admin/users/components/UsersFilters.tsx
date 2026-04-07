"use client";

import { useState, useEffect } from "react";

// Definição da Interface para evitar o erro de "Unexpected any"
interface UsersFiltersProps {
  role: string;
  status: string;
  search: string;
  onChange: (key: string, value: string) => void;
}

export function UsersFilters({
  role,
  status,
  search,
  onChange
}: UsersFiltersProps) {

  // Estado local para o input de busca (evita travamentos na digitação)
  const [searchValue, setSearchValue] = useState(search);

  // Efeito de Debounce: Espera o usuário parar de digitar por 500ms 
  // antes de disparar a busca no Backend
  useEffect(() => {
    const delay = setTimeout(() => {
      onChange("search", searchValue);
    }, 500);

    return () => clearTimeout(delay);
  }, [searchValue, onChange]);

  return (
    <div className="flex gap-3 flex-wrap bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">

      {/* INPUT DE BUSCA */}
      <input
        placeholder="Buscar por e-mail ou nome..."
        value={searchValue}
        onChange={(e) => setSearchValue(e.target.value)}
        className="px-4 py-2 border rounded-xl text-sm w-72 dark:bg-slate-950 border-slate-200 dark:border-slate-700 outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
      />

      {/* FILTRO DE CARGO (ROLE) - Sincronizado com UserRole Backend */}
      <select
        value={role}
        onChange={(e) => onChange("role", e.target.value)}
        className="px-3 py-2 border rounded-xl text-sm bg-white dark:bg-slate-950 border-slate-200 dark:border-slate-700 outline-none focus:ring-2 focus:ring-blue-500 dark:text-white cursor-pointer"
      >
        <option value="">Todos Perfis</option>
        <optgroup label="Administrativo">
          <option value="admin_master">Admin Master</option>
          <option value="gerente">Gerente</option>
          <option value="administrativo">Financeiro/Adm</option>
        </optgroup>
        <optgroup label="Operacional">
          <option value="suporte">Suporte</option>
          <option value="marketing">Marketing</option>
          <option value="gestor_interno">Gestor Interno</option>
        </optgroup>
        <optgroup label="Clientes">
          <option value="gestor_assinante">Assinante (Gestor)</option>
          <option value="cliente_final">Cliente Final</option>
        </optgroup>
      </select>

      {/* FILTRO DE STATUS - Sincronizado com UserStatus Backend */}
      <select
        value={status}
        onChange={(e) => onChange("status", e.target.value)}
        className="px-3 py-2 border rounded-xl text-sm bg-white dark:bg-slate-950 border-slate-200 dark:border-slate-700 outline-none focus:ring-2 focus:ring-blue-500 dark:text-white cursor-pointer"
      >
        <option value="">Todos Status</option>
        <option value="active">Ativo</option>
        <option value="pending_invite">Convite Pendente</option>
        <option value="blocked">Bloqueado</option>
        <option value="inactive">Inativo</option>
      </select>

    </div>
  );
}
