import { useState, useCallback } from "react";
import api from "@/services/api";

export function useAdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchUsers = useCallback(async (filter?: string) => {
    setLoading(true);
    try {
      const url = filter ? `/admin/users?filter=${filter}` : "/admin/users";
      const { data } = await api.get(url);
      setUsers(data);
    } finally {
      setLoading(false);
    }
  }, []);

  const resetPassword = async (userId: number) => {
    const { data } = await api.post(`/admin/users/${userId}/reset-password`);
    alert(`Senha resetada! Nova senha: ${data.temp_password}`);
    return data.temp_password;
  };

  const grantAccess = async (userId: number, days: number) => {
    await api.post(`/admin/users/${userId}/grant-access`, { days });
    fetchUsers(); // Atualiza a lista
  };

  return { users, loading, fetchUsers, resetPassword, grantAccess };
}
