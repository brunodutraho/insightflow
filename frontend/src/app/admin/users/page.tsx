"use client";

import UsersTable from "../components/UsersTable";
import { useUser } from "@/hooks/useUser";

export default function UsersPage() {
  const { user } = useUser();

  // 🔒 proteção
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
      <h1 className="text-2xl font-bold">Usuários</h1>

      <UsersTable />
    </div>
  );
}