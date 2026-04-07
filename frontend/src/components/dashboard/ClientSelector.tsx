"use client";
import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import api from "@/services/api";
import { useUser } from "@/hooks/useUser";

export default function ClientSelector() {
  const { user } = useUser();
  const router = useRouter();
  const searchParams = useSearchParams();
  // 1. Atualizado: id agora é string (UUID)
  const [clients, setClients] = useState<{ id: string; name: string }[]>([]);
  const [mounted, setMounted] = useState(false);

  const currentClientId = searchParams.get("client_id") || "";

  // 2. ATUALIZADO: Quem pode trocar de cliente na visão geral?
  // Agora Master, Gerente e os Gestores (Interno e Assinante) podem ver seus clientes
  const canSelect = user && [
    "admin_master", 
    "gerente", 
    "gestor_interno", 
    "gestor_assinante"
  ].includes(user.role);

  useEffect(() => {
    setMounted(true);
    if (mounted && canSelect) {
      // Busca a lista de tenants/clientes que o usuário tem acesso
      api.get("/admin/clients") 
        .then((res) => setClients(res.data))
        .catch(err => console.error("Erro ao carregar clientes:", err));
    }
  }, [canSelect, mounted]);

  if (!mounted || !canSelect) return null;

  return (
    <select 
      value={currentClientId}
      onChange={(e) => {
        const id = e.target.value;
        // 3. Atualizado: Mantém o client_id na URL para filtrar os dashboards
        if (id) router.push(`/dashboard?client_id=${id}`);
      }}
      className="bg-slate-800 text-white text-sm border border-slate-700 rounded-md px-3 py-1 outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer hover:bg-slate-700 transition-colors"
    >
      <option value="" disabled>Selecionar Cliente</option>
      {clients.map((c) => (
        <option key={c.id} value={c.id} className="bg-slate-900">
          {c.name}
        </option>
      ))}
    </select>
  );
}
