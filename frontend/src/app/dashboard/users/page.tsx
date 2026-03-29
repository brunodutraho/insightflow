"use client";

import { useState, useEffect } from "react";
import { useUser } from "@/hooks/useUser";
import api from "@/services/api";
import { UserPlus, ShieldCheck, Mail, Building } from "lucide-react";

export default function ManageUsersPage() {
  const { user } = useUser();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [clientId, setClientId] = useState("");
  const [message, setMessage] = useState({ text: "", type: "" });
  const [loading, setLoading] = useState(false);

  // 🛡️ Proteção de Interface: Cliente final não vê nada aqui
  if (user.role === "cliente") {
    return (
      <div className="p-8 bg-red-900/20 border border-red-500/50 rounded-xl text-red-500">
        Acesso restrito para Gestores e Administradores.
      </div>
    );
  }

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: "", type: "" });

    try {
      await api.post("/auth/create-client-access", {
        email,
        password,
        client_id: Number(clientId)
      });
      
      setMessage({ 
        text: "Acesso Premium criado! O cliente já pode logar com estas credenciais.", 
        type: "success" 
      });
      setEmail("");
      setPassword("");
      setClientId("");
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || "Erro ao criar acesso.";
      setMessage({ text: errorMsg, type: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">
        <header className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <UserPlus className="text-blue-500" size={24} />
            </div>
            <h1 className="text-2xl font-bold text-white">Novo Acesso Cliente</h1>
          </div>
          <p className="text-slate-400 text-sm italic">
            Crie um login exclusivo para o seu cliente visualizar as métricas da empresa dele.
          </p>
        </header>

        <form onSubmit={handleCreateUser} className="space-y-5">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase flex items-center gap-2">
              <Mail size={14} /> E-mail do Usuário
            </label>
            <input 
              type="email" 
              className="w-full bg-slate-950 border border-slate-800 p-3 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-white transition-all"
              placeholder="cliente@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase flex items-center gap-2">
              <ShieldCheck size={14} /> Senha de Acesso
            </label>
            <input 
              type="password" 
              className="w-full bg-slate-950 border border-slate-800 p-3 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-white transition-all"
              placeholder="Defina uma senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase flex items-center gap-2">
              <Building size={14} /> ID da Empresa (Client ID)
            </label>
            <input 
              type="number" 
              className="w-full bg-slate-950 border border-slate-800 p-3 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-white transition-all"
              placeholder="Ex: 1"
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
              required
            />
          </div>

          <button 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-bold py-3.5 rounded-lg transition-all shadow-lg shadow-blue-900/20 mt-4"
          >
            {loading ? "Processando..." : "Gerar Acesso e Vincular"}
          </button>

          {message.text && (
            <div className={`p-4 rounded-lg text-sm text-center border animate-in zoom-in-95 duration-300 ${
              message.type === "success" 
                ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" 
                : "bg-red-500/10 text-red-500 border-red-500/20"
            }`}>
              {message.text}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
