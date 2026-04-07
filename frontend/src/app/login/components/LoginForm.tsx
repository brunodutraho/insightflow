"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/services/auth.service";
import Cookies from "js-cookie";
import Link from "next/link";
import { Mail, Lock, ArrowRight, Loader2, Rocket } from "lucide-react";

export default function LoginForm() {
const router = useRouter();

const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

async function handleLogin(e: React.FormEvent) {
  e.preventDefault();


  if (!email.trim() || !password.trim()) {
    setError("Por favor, preencha email e senha");
    return;
  }

  setLoading(true);
  setError("");

  try {
    const data = await login({ email: email.trim(), password });

    if (!data.access_token) {
      throw new Error("Token não recebido do servidor");
    }

    const token = data.access_token;

    // 🔐 Cookie
    Cookies.set("token", token, {
      expires: 1,
      path: "/",
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
    });

    // ⚙️ LocalStorage
    localStorage.setItem("token", token);

    // 🎯 Decode token
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const role = payload.role;

      if (!role) {
        throw new Error("Token inválido - role não encontrada");
      }

      const roleRoutes: Record<string, string> = {
        admin_master: "/admin",
        gerente: "/dashboard",
        administrativo: "/finance",
        suporte: "/support",
        marketing: "/marketing",
        gestor_assinante: "/dashboard",
        user: "/dashboard",
      };

      const redirectPath = roleRoutes[role] || "/dashboard";
      router.push(redirectPath);
    } catch (tokenError) {
      console.error("Token decode error:", tokenError);

      setError("Erro ao processar autenticação. Tente novamente.");

      localStorage.removeItem("token");
      Cookies.remove("token");
    }
  } catch (error: any) {
    console.error("Login error:", error);

    if (error.response?.status === 401) {
      setError("Email ou senha incorretos");
    } 
    else if (error.response?.status === 403) {
      const detail = error.response?.data?.detail;

      // 🔥 TRATAMENTO PROFISSIONAL DO EMAIL NÃO VERIFICADO
      if (typeof detail === "object" && detail?.message === "EMAIL_NOT_VERIFIED") {
        const emailEncoded = encodeURIComponent(detail.email);

        router.push(`/verify-email?email=${emailEncoded}`);
        return;
      }

      setError(
        typeof detail === "string"
          ? detail
          : "Conta não autorizada"
      );
    } 
    else if (error.response?.status === 422) {
      setError("Dados inválidos. Verifique email e senha");
    } 
    else if (error.response?.data?.detail) {
      setError(error.response.data.detail);
    } 
    else if (error.message) {
      setError(error.message);
    } 
    else {
      setError("Erro ao fazer login. Tente novamente.");
    }
  } finally {
    setLoading(false);
  }

}

return ( <div className="min-h-screen bg-brand-dark flex items-center justify-center p-6"> <div className="w-full max-w-md animate-fade-in">


      {/* LOGO */}
      <div className="flex flex-col items-center mb-10">
        <div className="bg-brand-primary p-3 rounded-2xl mb-4 shadow-[0_0_25px_rgba(124,58,237,0.4)]">
          <Rocket size={30} className="text-white" />
        </div>

        <h1 className="text-3xl font-black text-white tracking-tight">
          InsightFlow
        </h1>

        <p className="text-brand-muted text-sm mt-2">
          Inteligência para decisões de marketing
        </p>
      </div>

      {/* CARD */}
      <div className="bg-brand-surface border border-brand-border p-8 rounded-3xl shadow-xl">

        <h2 className="text-xl font-semibold text-white mb-1">
          Bem-vindo de volta
        </h2>

        <p className="text-brand-muted text-sm mb-8">
          Entre com suas credenciais para acessar o painel
        </p>

        <form onSubmit={handleLogin} className="space-y-5">

          {error && (
            <div className="bg-brand-danger/10 border border-brand-danger/30 text-brand-danger p-3 rounded-xl text-xs text-center">
              {error}
            </div>
          )}

          {/* EMAIL */}
          <div className="space-y-2">
            <label className="text-[10px] uppercase font-bold text-brand-muted tracking-widest">
              E-mail
            </label>

            <div className="relative">
              <Mail
                className="absolute left-3 top-1/2 -translate-y-1/2 text-brand-muted"
                size={18}
              />

              <input
                type="email"
                className="w-full bg-brand-dark border border-brand-border rounded-xl py-3 pl-11 pr-4 outline-none focus:ring-2 focus:ring-brand-primary text-white transition-all"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          {/* PASSWORD */}
          <div className="space-y-2">
            <label className="text-[10px] uppercase font-bold text-brand-muted tracking-widest">
              Senha
            </label>

            <div className="relative">
              <Lock
                className="absolute left-3 top-1/2 -translate-y-1/2 text-brand-muted"
                size={18}
              />

              <input
                type="password"
                className="w-full bg-brand-dark border border-brand-border rounded-xl py-3 pl-11 pr-4 outline-none focus:ring-2 focus:ring-brand-primary text-white transition-all"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          {/* BUTTON */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-brand-primary hover:opacity-90 text-white font-bold py-4 rounded-2xl flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            {loading ? (
              <Loader2 className="animate-spin" />
            ) : (
              <>
                Acessar painel <ArrowRight size={18} />
              </>
            )}
          </button>
        </form>
      </div>

      {/* REGISTER */}
      <p className="mt-8 text-center text-brand-muted text-sm">
        Não tem uma conta?{" "}
        <Link
          href="/register"
          className="text-brand-primary font-semibold hover:underline"
        >
          Criar conta grátis
        </Link>
      </p>
    </div>
  </div>
  );
}
