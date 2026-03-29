"use client";

import { useUser } from "@/hooks/useUser";
import { useEffect, useState } from "react";
import api from "@/services/api";

type AdminData = {
  summary: {
    total_users: number;
    total_companies: number;
  };
  distribution: {
    role: string;
    count: number;
  }[];
};

export default function AdminPage() {
  const { user } = useUser();

  const [data, setData] = useState<AdminData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await api.get("/admin/stats");
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!user) return null;

  if (user.role !== "admin") {
    return <div>Acesso restrito</div>;
  }

  return (
    <div className="space-y-8">

      <header>
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      </header>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div className="bg-gray-100 dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-xl">
          <p className="text-sm text-gray-500">Usuários</p>
          <h2 className="text-3xl font-bold">
            {data?.summary.total_users}
          </h2>
        </div>

        <div className="bg-gray-100 dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-xl">
          <p className="text-sm text-gray-500">Empresas</p>
          <h2 className="text-3xl font-bold">
            {data?.summary.total_companies}
          </h2>
        </div>

      </div>

    </div>
  );
}