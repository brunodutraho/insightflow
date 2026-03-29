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

    setLoading(true);
    setError("");

    try {
      const data = await login({ email, password });
      const token = data.access_token;

      // 🔐 Cookie
      Cookies.set("token", token, {
        expires: 1,
        path: "/",
      });

      // ⚙️ LocalStorage
      localStorage.setItem("token", token);

      // 🎯 Decodifica token (role)
      const payload = JSON.parse(atob(token.split(".")[1]));
      const role = payload.role;

      // 🚀 Redirecionamento
      if (role === "admin") {
        router.push("/admin");
      } else if (role === "gestor") {
        router.push("/dashboard");
      } else {
        router.push("/analytics");
      }

    } catch (err) {
      setError("Credenciais inválidas. Verifique seu e-mail e senha.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-brand-dark flex items-center justify-center p-6">
      <div className="w-full max-w-md animate-fade-in">

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

        {/* REGISTER LINK */}
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