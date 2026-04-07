"use client";

import { useState } from "react";
import api from "@/services/api";
import {
  X,
  KeyRound,
  Gift,
  Mail,
  User as UserIcon,
  Lock,
  Loader2,
  ChevronRight
} from "lucide-react";

interface User {
  id: string;
  email: string;
  role: string;
  status: string;
  tenant_id: string;
  full_name: string | null;
  // Campos estendidos que o Admin costuma enviar:
  plan_name?: string; 
  last_login_days?: number | null;
}

export function UserDrawer({
  user,
  onClose,
  onUpdate
}: {
  user: User | null;
  onClose: () => void;
  onUpdate: () => void;
}) {
  const [confirmingAction, setConfirmingAction] = useState<
    "reset" | "bonus" | "block" | "resend" | "delete" | null
  >(null);

  const [adminPassword, setAdminPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // Se não houver usuário, não renderiza nada
  if (!user) return null;

  async function handleConfirmAction() {
    // Pegamos o ID em uma constante local para o TS parar de reclamar do 'null'
    const userId = user?.id; 
    if (!userId || !adminPassword) return;

    setLoading(true);

    try {
      if (confirmingAction === "reset") {
        const res = await api.post(
          `/admin/users/${userId}/reset-password`,
          { password: adminPassword }
        );
        alert("🚀 SENHA TEMPORÁRIA: " + res.data.temp_password);
      }

      else if (confirmingAction === "bonus") {
        await api.post(`/admin/users/${userId}/grant-access`, {
          days: 30,
          password: adminPassword
        });
        alert("🎁 30 dias de bônus aplicados!");
      }

      else if (confirmingAction === "block") {
        await api.patch(`/admin/users/${userId}/block`, {
          password: adminPassword
        });
        alert(user.status === "blocked" ? "🔓 Usuário desbloqueado!" : "🔒 Usuário bloqueado!");
      }

      else if (confirmingAction === "resend") {
        await api.post(`/admin/users/${userId}/resend-verification`, {
          password: adminPassword
        });
        alert("📩 Email de verificação reenviado!");
      }

      setConfirmingAction(null);
      setAdminPassword("");
      onUpdate();

    } catch (err: any) {
      alert(err.response?.data?.detail || "Erro na operação.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex justify-end">

      {/* Overlay */}
      <div
        className="absolute inset-0 bg-slate-950/40 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* 🔐 MODAL DE CONFIRMAÇÃO */}
      {confirmingAction && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-surface p-8 rounded-[2.5rem] shadow-2xl border w-full max-w-sm">

            <div className="flex flex-col items-center text-center">

              <div className="w-14 h-14 bg-brand-primary/10 text-brand-primary rounded-full flex items-center justify-center mb-6">
                <Lock size={28} />
              </div>

              <h3 className="font-black uppercase text-sm tracking-[0.2em] mb-2">
                Confirmação Admin
              </h3>

              <p className="text-xs text-slate-500 mb-8">
                Digite sua senha para continuar
              </p>

              <input
                type="password"
                autoFocus
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                onKeyDown={(e) =>
                  e.key === "Enter" && handleConfirmAction()
                }
                placeholder="Sua senha"
                className="w-full p-4 border rounded-2xl text-center font-bold mb-6"
              />

              <div className="flex gap-3 w-full">
                <button
                  onClick={() => {
                    setConfirmingAction(null);
                    setAdminPassword("");
                  }}
                  className="flex-1 py-3 text-xs font-bold uppercase"
                >
                  Cancelar
                </button>

                <button
                  onClick={handleConfirmAction}
                  disabled={loading || !adminPassword}
                  className="flex-1 py-3 bg-brand-primary text-white text-xs font-bold rounded-xl flex justify-center items-center"
                >
                  {loading ? (
                    <Loader2 className="animate-spin" size={18} />
                  ) : (
                    "Confirmar"
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* DRAWER */}
      <div className="relative w-full max-w-[420px] h-full bg-white dark:bg-brand-surface shadow-2xl border-l flex flex-col">

        {/* HEADER */}
        <div className="p-6 border-b flex justify-between items-center">
          <div className="flex items-center gap-3">
            <UserIcon size={20} />
            <h2 className="text-sm font-black uppercase">
              Usuário
            </h2>
          </div>

          <button onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* CONTEÚDO */}
        <div className="flex-1 overflow-y-auto p-8 space-y-10">

          {/* IDENTIDADE */}
          <div className="flex items-center gap-5">
            <div className="w-20 h-20 rounded-2xl bg-brand-primary text-white flex items-center justify-center text-2xl font-black">
              {user.email.charAt(0).toUpperCase()}
            </div>

            <div>
              <p className="font-bold text-lg">{user.email}</p>

              <span className="text-xs text-slate-500">
                {user.role}
              </span>
            </div>
          </div>

          {/* INFO */}
          <div className="space-y-4 text-sm">

            <div>
              <p className="text-xs text-slate-400">Status</p>
              <p className="font-bold">{user.status}</p>
            </div>

            <div>
              <p className="text-xs text-slate-400">Plano</p>
              <p className="font-bold">{user.plan_name || "Free"}</p>
            </div>

            <div>
              <p className="text-xs text-slate-400">Último acesso</p>
              <p className="font-bold">
                {user.last_login_days !== null
                  ? `${user.last_login_days} dias atrás`
                  : "Nunca"}
              </p>
            </div>

          </div>

          {/* AÇÕES */}
          <div className="space-y-4">

            <button
              onClick={() => setConfirmingAction("reset")}
              className="w-full flex justify-between p-4 border rounded-xl"
            >
              <div className="flex gap-3 items-center">
                <KeyRound size={18} />
                Resetar senha
              </div>
              <ChevronRight size={16} />
            </button>

            <button
              onClick={() => setConfirmingAction("resend")}
              className="w-full flex justify-between p-4 border rounded-xl"
            >
              <div className="flex gap-3 items-center">
                <Mail size={18} />
                Reenviar verificação
              </div>
              <ChevronRight size={16} />
            </button>

            <button
              onClick={() => setConfirmingAction("bonus")}
              className="w-full flex justify-between p-4 border rounded-xl text-emerald-600"
            >
              <div className="flex gap-3 items-center">
                <Gift size={18} />
                Bonificar 30 dias
              </div>
              <ChevronRight size={16} />
            </button>

          </div>

          {/* PERIGO */}
          <div className="space-y-4 pt-6">

            <button
              onClick={() => setConfirmingAction("block")}
              className="w-full p-4 rounded-xl bg-rose-500 text-white font-bold"
            >
              {user.status === "blocked"
                ? "Desbloquear usuário"
                : "Bloquear usuário"}
            </button>

          </div>

        </div>

        {/* FOOTER */}
        <div className="p-6 border-t text-center text-xs text-slate-400">
          ID: {user.id}
        </div>

      </div>
    </div>
  );
}