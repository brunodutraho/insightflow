"use client";

import CompaniesTable from "../components/CompaniesTable";
import { useUser } from "@/hooks/useUser";

export default function CompaniesPage() {
  const { user } = useUser();

  if (!user) return null;

  if (user.role !== "admin") {
    return (
      <div className="flex h-screen items-center justify-center text-white">
        <h1 className="text-xl font-bold text-red-500">
          403 | Acesso restrito
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Empresas</h1>

      <CompaniesTable />
    </div>
  );
}