"use client";

import { useState, useEffect, useCallback } from "react"; // Adicionado useCallback
import { verifyEmail, resendCode } from "@/services/auth.service";
import { useRouter } from "next/navigation";

export default function VerifyEmailForm({ email }: { email: string }) {
  const [token, setToken] = useState("");
  const [error, setError] = useState("");
  const [cooldown, setCooldown] = useState(60);
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  // countdown - Sem alterações, está perfeito
  useEffect(() => {
    if (cooldown <= 0) return;
    const interval = setInterval(() => {
      setCooldown((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [cooldown]);

  // handleVerify envolvido em useCallback para calar o ESLint e evitar re-renders
  const handleVerify = useCallback(async () => {
    if (loading) return;
    
    try {
      setLoading(true);
      setError("");

      const res = await verifyEmail({ token });

      if (res?.access_token) {
        router.push("/choose-plan");
      } else {
        throw new Error();
      }
    } catch {
      setError("Código inválido ou expirado");
      setToken(""); // Limpa o campo para o usuário tentar de novo
    } finally {
      setLoading(false);
    }
  }, [token, loading, router]); // Dependências da função

  // auto-submit corrigido com handleVerify na dependência
  useEffect(() => {
    if (token.length === 6) {
      handleVerify();
    }
  }, [token, handleVerify]);

  async function handleResend() {
    try {
      await resendCode(email);
      setCooldown(60);
      setToken("");
      setError("");
    } catch {
      setError("Erro ao reenviar");
    }
  }

  return (
    <div className="max-w-md w-full bg-slate-900 p-10 rounded-3xl border border-slate-800 text-center">
      <h2 className="text-2xl font-bold text-white mb-4">Verifique seu email</h2>
      <p className="text-slate-400 mb-6">
        Código enviado para <br />
        <strong>{email}</strong>
      </p>

      <input
        value={token}
        onChange={(e) => setToken(e.target.value.replace(/\D/g, ""))}
        maxLength={6}
        disabled={loading} // Travamos o input durante o loading
        placeholder="000000"
        className={`w-full text-center text-2xl tracking-[10px] p-4 bg-slate-800 rounded-xl text-white transition-opacity ${
          loading ? "opacity-50 cursor-not-allowed" : "opacity-100"
        }`}
      />

      {error && <p className="text-red-500 mt-4 text-sm">{error}</p>}

      {loading && (
        <div className="mt-4 flex items-center justify-center gap-2 text-blue-500 text-sm">
          <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          Verificando...
        </div>
      )}

      <button
        type="button"
        disabled={cooldown > 0 || loading}
        onClick={handleResend}
        className="mt-8 text-sm text-blue-500 disabled:text-gray-600 transition-colors hover:text-blue-400"
      >
        {cooldown > 0
          ? `Reenviar código em ${cooldown}s`
          : "Não recebeu o código? Reenviar"}
      </button>
    </div>
  );
}
