"use client";

import { useState } from "react";
import api from "@/services/api";

type Props = {
  onSuccess: () => void;
  onClose: () => void;
};

export default function ReauthModal({ onSuccess, onClose }: Props) {
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleConfirm() {
    setLoading(true);
    setError("");

    try {
      await api.post("/auth/reauth", { password });
      onSuccess();
    } catch (err) {
      setError("Senha incorreta");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-slate-900 p-6 rounded-lg w-80 space-y-4 shadow-lg">

        <h2 className="text-lg font-bold">Confirmar senha</h2>

        <input
          type="password"
          placeholder="Digite sua senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded bg-white dark:bg-slate-800"
        />

        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-3 py-2 text-sm"
          >
            Cancelar
          </button>

          <button
            onClick={handleConfirm}
            disabled={loading}
            className="bg-blue-500 text-white px-3 py-2 rounded text-sm"
          >
            {loading ? "Verificando..." : "Confirmar"}
          </button>
        </div>

      </div>
    </div>
  );
}