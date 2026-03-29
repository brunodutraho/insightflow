"use client";
import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import api from "@/services/api";
import { useUser } from "@/hooks/useUser";

export default function ClientSelector() {
  const { user } = useUser();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [clients, setClients] = useState<{ id: number; name: string }[]>([]);
  const [mounted, setMounted] = useState(false); // Trava de hidratação

  const currentClientId = searchParams.get("client_id") || "";
  const canSelect = user?.role === "admin" || user?.role === "gestor";

  useEffect(() => {
    setMounted(true); // Só vira true no navegador
    if (canSelect) {
      api.get("/clients/").then((res) => setClients(res.data));
    }
  }, [canSelect]);

  // Se não estiver montado ou não puder selecionar, não renderiza nada no Servidor
  if (!mounted || !canSelect) return null;

  return (
    <select 
      value={currentClientId}
      onChange={(e) => {
        const id = e.target.value;
        if (id) router.push(`/dashboard?client_id=${id}`);
      }}
      className="bg-slate-800 text-white text-sm border border-slate-700 rounded-md px-3 py-1 outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
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
