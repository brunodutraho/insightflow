"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { 
  Rocket, ArrowLeft, MailCheck, Loader2, Eye, EyeOff, ShieldCheck
} from "lucide-react";
import { FcGoogle } from "react-icons/fc";
import { FaApple, FaMicrosoft } from "react-icons/fa6";
import axios from "axios";

// Instância local rápida para garantir funcionamento
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

export default function RegisterPage() {
  const router = useRouter();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isRegistered, setIsRegistered] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // ESTADO DOS DADOS QUE O SEU ADMIN VAI PUXAR NO BACKEND
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    confirmEmail: "",
    password: "",
    phone: "",
    company_name: "",
    team_size: "",
    how_heard: "",
    terms: false,
  });

  useEffect(() => { setMounted(true); }, []);

  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
    if (error) setError("");
  };

  // REDIRECIONAMENTO OAUTH (GOOGLE/MS/APPLE)
  const handleSocialRegister = (provider: string) => {
    window.location.href = `http://localhost:8000/auth/login/${provider}`;
  };

  // ENVIO PARA O SERVIDOR (CAPTURA REAL)
  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();

    if (formData.email !== formData.confirmEmail) return setError("E-mails não coincidem.");
    if (!formData.terms) return setError("Aceite os termos para continuar.");
    if (formData.password.length < 8) return setError("Senha deve ter no mínimo 8 caracteres.");

    setLoading(true);

    try {
      // Payload idêntico ao que o seu banco espera (User + Tenant)
      const payload = {
        full_name: formData.name,
        email: formData.email.trim().toLowerCase(),
        password: formData.password,
        phone: formData.phone,
        company_name: formData.company_name,
        team_size: Number(formData.team_size),
        how_heard: formData.how_heard,
        terms_accepted: formData.terms
      };

      await api.post("/auth/register", payload);

      // salva email pro fluxo
      localStorage.setItem("email", formData.email);

      router.push(`/verify-email`);
      window.scrollTo(0, 0);

    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao cadastrar. Verifique os dados ou se o e-mail já existe.");
    } finally {
      setLoading(false);
    }
  }

  if (!mounted) return null;

  // --- TELA 2: CONFIRMAÇÃO DE E-MAIL (PÓS-CADASTRO) ---
  if (isRegistered) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 p-6">
        <div className="max-w-md w-full bg-slate-900 border border-slate-800 p-10 rounded-[3rem] shadow-2xl text-center">
          <div className="w-20 h-20 bg-blue-600/20 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-8 animate-bounce">
            <MailCheck size={40} />
          </div>
          <h2 className="text-3xl font-black text-white mb-4 italic uppercase tracking-tighter italic">Verifique seu E-mail</h2>
          <p className="text-slate-400 text-sm leading-relaxed mb-10">
            Cadastro realizado! Enviamos um link de ativação para: <br/>
            <strong className="text-blue-400 font-bold">{formData.email}</strong>. <br/><br/>
            Clique no link para validar sua conta e liberar o acesso ao painel.
          </p>
          <Link href="/login" className="block w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl transition-all">
            Ir para o Login
          </Link>
        </div>
      </div>
    );
  }

  // --- TELA 1: FORMULÁRIO DE CADASTRO ---
  return (
    <div className="flex items-center justify-center min-h-screen bg-slate-950 p-4 py-20">
      <div className="w-full max-w-[700px]">
        
        <Link href="/" className="inline-flex items-center gap-2 text-slate-500 mb-8 text-xs font-bold hover:text-white transition-colors">
          <ArrowLeft size={14} /> Voltar para o Site
        </Link>

        <div className="bg-slate-900 p-8 md:p-12 rounded-[2.5rem] border border-slate-800 shadow-2xl">
          
          <div className="flex flex-col items-center mb-10 text-center">
            <div className="bg-blue-600 p-4 rounded-2xl mb-4 shadow-lg shadow-blue-600/30">
              <Rocket size={32} className="text-white" />
            </div>
            <h2 className="text-4xl font-black text-white italic uppercase tracking-tighter italic">InsightFlow</h2>
            <p className="text-slate-500 text-sm font-medium mt-2 uppercase tracking-[0.2em]">Crie sua conta gratuita</p>
          </div>

          {/* LOGIN SOCIAL NO TOPO */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-10">
            <button type="button" onClick={() => handleSocialRegister('google')} className="flex items-center justify-center gap-3 bg-white hover:bg-slate-200 p-3 rounded-xl transition-all">
              <FcGoogle size={20} /> <span className="text-xs font-bold text-black">Google</span>
            </button>
            <button type="button" onClick={() => handleSocialRegister('microsoft')} className="flex items-center justify-center gap-3 bg-white hover:bg-slate-200 p-3 rounded-xl transition-all">
              <FaMicrosoft size={18} className="text-blue-600" /> <span className="text-xs font-bold text-black">Outlook</span>
            </button>
            <button type="button" onClick={() => handleSocialRegister('apple')} className="flex items-center justify-center gap-3 bg-white hover:bg-slate-200 p-3 rounded-xl transition-all">
              <FaApple size={20} className="text-black" /> <span className="text-xs font-bold text-black">Apple</span>
            </button>
          </div>

          <div className="relative flex py-5 items-center">
            <div className="flex-grow border-t border-slate-800"></div>
            <span className="flex-shrink mx-4 text-[10px] font-black text-slate-600 uppercase tracking-[0.3em]">Ou preencha abaixo</span>
            <div className="flex-grow border-t border-slate-800"></div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-500 text-xs font-bold flex items-center gap-3 animate-pulse">
              <ShieldCheck size={18} /> {error}
            </div>
          )}

          <form onSubmit={handleRegister} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">Nome Completo</label>
                <input required name="name" value={formData.name} onChange={handleChange} placeholder="Seu nome" className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all" />
              </div>
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">Nome da Empresa</label>
                <input required name="company_name" value={formData.company_name} onChange={handleChange} placeholder="Nome do seu negócio" className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all" />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">E-mail Corporativo</label>
                <input required type="email" name="email" value={formData.email} onChange={handleChange} placeholder="seu@email.com" className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all" />
              </div>
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">Confirmar E-mail</label>
                <input required type="email" name="confirmEmail" value={formData.confirmEmail} onChange={handleChange} placeholder="Repita o e-mail" className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all" />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="relative space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">Crie uma Senha</label>
                <input required type={showPassword ? "text" : "password"} name="password" value={formData.password} onChange={handleChange} placeholder="Mín. 8 caracteres" className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all" />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-4 top-10 text-slate-500 hover:text-white">
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">WhatsApp / Celular</label>
                <input required name="phone" value={formData.phone} onChange={handleChange} placeholder="(00) 00000-0000" className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all" />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">Tamanho do Time</label>
                <select name="team_size" value={formData.team_size} onChange={handleChange} className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all appearance-none cursor-pointer">
                  <option value="">Selecione...</option>
                  <option value="1">Apenas eu</option>
                  <option value="5">2 a 5 pessoas</option>
                  <option value="20">6 a 20 pessoas</option>
                  <option value="50">Mais de 20 pessoas</option>
                </select>
              </div>
              <div className="space-y-1">
                <label className="text-[10px] uppercase font-black text-slate-500 ml-2 tracking-widest">Como nos conheceu?</label>
                <select name="how_heard" value={formData.how_heard} onChange={handleChange} className="w-full bg-slate-800/50 border-slate-700 rounded-2xl p-4 text-white text-sm outline-none focus:ring-2 focus:ring-blue-600 transition-all appearance-none cursor-pointer">
                  <option value="">Selecione...</option>
                  <option value="google">Google</option>
                  <option value="instagram">Instagram</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="indicacao">Indicação</option>
                </select>
              </div>
            </div>

            <div className="p-4 bg-slate-800/30 rounded-2xl border border-slate-800 space-y-3">
              <div className="flex items-start gap-3">
                <input required type="checkbox" name="terms" checked={formData.terms} onChange={handleChange} className="mt-1 w-4 h-4 accent-blue-600 cursor-pointer" id="terms" />
                <label htmlFor="terms" className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter leading-tight">
                  Eu li e aceito os <Link href="/terms" className="text-blue-500 underline">Termos de Uso</Link> e a <Link href="/privacy" className="text-blue-500 underline">Política de Privacidade</Link> do InsightFlow.
                </label>
              </div>
            </div>

            <button disabled={loading} className="w-full py-5 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-800 text-white font-black uppercase tracking-[0.2em] text-xs rounded-2xl transition-all shadow-xl shadow-blue-600/20 flex justify-center items-center gap-3">
              {loading ? <Loader2 className="animate-spin" size={20} /> : "Finalizar Cadastro Grátis"}
            </button>

            <p className="text-center text-slate-500 text-xs font-bold">
              Já é de casa? <Link href="/login" className="text-blue-500 hover:underline">Faça login</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
