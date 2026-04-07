"use client";

import api from "@/services/api";
import { useEffect, useState } from "react";

// 1. Atualizado: ID agora é string (UUID)
type User = {
  id: string; 
  email: string;
  role: string;
};

export default function UsersTable() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  async function fetchUsers() {
    try {
      const token = localStorage.getItem("token");
      const res = await api.get("/users", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(res.data);
    } catch (err) {
      console.error("Erro ao buscar usuários:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchUsers();
  }, []);

  // 2. Atualizado: id é string e payload mudou para bater com o backend (new_role)
  async function changeRole(id: string, newRole: string) {
    try {
      const token = localStorage.getItem("token");
      await api.patch(
        `/users/${id}/role`,
        { new_role: newRole }, // O backend agora espera 'new_role' conforme corrigimos
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchUsers();
    } catch (err) {
      console.error("Erro ao alterar role:", err);
      alert("Erro ao alterar cargo. Verifique suas permissões.");
    }
  }

  async function deleteUser(id: string) {
    if (!confirm("Tem certeza que deseja deletar este usuário?")) return;
    
    try {
      const token = localStorage.getItem("token");
      await api.delete(`/users/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchUsers();
    } catch (err) {
      console.error("Erro ao deletar usuário:", err);
    }
  }

  if (loading) return <div className="text-slate-400 p-6">Carregando usuários...</div>;

  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-xl shadow-sm">
      <h3 className="mb-4 font-bold text-lg">Gerenciamento de Usuários</h3>

      <table className="w-full text-sm">
        <thead className="text-slate-400 border-b border-gray-200 dark:border-slate-800">
          <tr>
            <th className="text-left pb-3">Email</th>
            <th className="text-center pb-3">Cargo (Role)</th>
            <th className="text-center pb-3">Ações</th>
          </tr>
        </thead>

        <tbody className="divide-y divide-gray-100 dark:divide-slate-800">
          {users.map((user) => (
            <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors">
              <td className="py-4">{user.email}</td>

              <td className="text-center py-4">
                <select
                  value={user.role}
                  onChange={(e) => changeRole(user.id, e.target.value)}
                  className="bg-white dark:bg-slate-900 border border-gray-300 dark:border-slate-700 p-1.5 rounded-md text-xs focus:ring-2 focus:ring-blue-500 outline-none"
                >
                  {/* 3. ATUALIZADO: Opções agora batem com o UserRole do Backend */}
                  <optgroup label="Equipe Interna">
                    <option value="admin_master">Admin Master</option>
                    <option value="gerente">Gerente</option>
                    <option value="suporte">Suporte</option>
                    <option value="marketing">Marketing</option>
                    <option value="gestor_interno">Gestor Interno</option>
                  </optgroup>
                  <optgroup label="Clientes">
                    <option value="gestor_assinante">Assinante (Gestor)</option>
                    <option value="cliente_final">Cliente do Gestor</option>
                  </optgroup>
                </select>
              </td>

              <td className="text-center py-4">
                <button
                  onClick={() => deleteUser(user.id)}
                  className="text-red-500 hover:text-red-700 font-medium transition-colors"
                >
                  Deletar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
