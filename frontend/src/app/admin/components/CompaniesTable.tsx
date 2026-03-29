"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";

export default function UsersTable() {
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  async function fetchUsers() {
    try {
      const res = await api.get("/admin/clients"); 
      setUsers(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="bg-gray-100 dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-xl">
      <h3 className="font-bold mb-4">Usuários</h3>

      {users.map((u) => (
        <div key={u.id} className="text-sm text-slate-400">
          {u.email} - {u.role}
        </div>
      ))}
    </div>
  );
}