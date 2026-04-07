"use client";

import { useEffect, useState, useCallback } from "react";
import api from "@/services/api";
import { useSearchParams, useRouter } from "next/navigation";

import { UsersHeader } from "./components/UsersHeader";
import { UsersFilters } from "./components/UsersFilters";
import { UsersTable } from "./components/UsersTable";
import { UsersTableSkeleton } from "./components/UsersTableSkeleton";
import { UsersEmptyState } from "./components/UsersEmptyState";
import { UserDrawer } from "./components/UserDrawer";

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

export default function UsersPage() {
  const searchParams = useSearchParams();
  const router = useRouter();

  // Pegando valores da URL
  const role = searchParams.get("role") || "";
  const status = searchParams.get("status") || "";
  const search = searchParams.get("search") || "";

  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // FUNÇÃO DE BUSCA REFORÇADA
  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);

      // Usar 'params' do Axios é melhor para lidar com caracteres especiais na busca
      const response = await api.get("/admin/users", {
        params: {
          role: role || undefined,
          status: status || undefined,
          search: search || undefined,
          _t: Date.now() // Força o navegador a não usar cache
        }
      });

      setUsers(response.data);
    } catch (err) {
      console.error("❌ Erro ao buscar usuários:", err);
      setUsers([]); // Em caso de erro, limpa a lista para não mostrar dados defasados
    } finally {
      setLoading(false);
    }
  }, [role, status, search]);

  // Dispara a busca sempre que os parâmetros da URL mudarem
  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  // Atualiza a URL sem recarregar a página inteira
  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());

    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }

    // scroll: false evita que a página pule para o topo ao filtrar
    router.push(`/admin/users?${params.toString()}`, { scroll: false });
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 min-h-screen">
      <UsersHeader />

      <UsersFilters
        role={role}
        status={status}
        search={search}
        onChange={updateFilter}
      />

      <div className="relative">
        {loading ? (
          <UsersTableSkeleton />
        ) : users.length === 0 ? (
          <UsersEmptyState />
        ) : (
          <UsersTable 
            users={users} 
            onSelect={(user) => setSelectedUser(user)} 
          />
        )}
      </div>

      {selectedUser && (
        <UserDrawer
          user={selectedUser}
          onClose={() => setSelectedUser(null)}
          onUpdate={fetchUsers}
        />
      )}
    </div>
  );
}
