"use client";

import api from "@/services/api";
import { useEffect, useState } from "react";

type User = {
  id: number;
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
        headers: {
          Authorization: `Bearer ${token}`,
        },
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

  async function changeRole(id: number, role: string) {
    try {
      const token = localStorage.getItem("token");

      await api.patch(
        `/users/${id}/role`,
        { role },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      fetchUsers();
    } catch (err) {
      console.error("Erro ao alterar role:", err);
    }
  }

  async function deleteUser(id: number) {
    try {
      const token = localStorage.getItem("token");

      await api.delete(`/users/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      fetchUsers();
    } catch (err) {
      console.error("Erro ao deletar usuário:", err);
    }
  }

  if (loading) {
    return (
      <div className="text-slate-400">
        Carregando usuários...
      </div>
    );
  }

  return (
    <div className="bg-gray-100 dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-xl">
      <h3 className="mb-4 font-bold">Usuários</h3>

      <table className="w-full text-sm">
        <thead className="text-slate-400">
          <tr>
            <th className="text-left">Email</th>
            <th className="text-center">Role</th>
            <th className="text-center">Ações</th>
          </tr>
        </thead>

        <tbody>
          {users.map((user) => (
            <tr key={user.id} className="border-t border-slate-800">
              <td>{user.email}</td>

              <td className="text-center">
                <select
                  value={user.role}
                  onChange={(e) =>
                    changeRole(user.id, e.target.value)
                  }
                  className="bg-gray-100 dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-1 rounded mb-1 mt-1 items-center justify-center"
                >
                  <option value="admin">Admin</option>
                  <option value="gestor">Gestor</option>
                  <option value="cliente">Cliente</option>
                </select>
              </td>

              <td className="text-center">
                <button
                  onClick={() => deleteUser(user.id)}
                  className="text-red-500 hover:underline"
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