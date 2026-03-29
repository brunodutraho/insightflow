"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Rocket, ArrowLeft, AlertCircle, Eye, EyeOff
} from "lucide-react";
import { FcGoogle } from "react-icons/fc";
import { FaApple, FaMicrosoft } from "react-icons/fa6";
import { TermsModal } from "@/components/Landing/TermsModal";
import { PolicyModal } from "@/components/Landing/PolicyModal";
import axios from "axios";


export default function RegisterPage() {
  const router = useRouter();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mounted, setMounted] = useState(false);
  
  const [showTerms, setShowTerms] = useState(false);
  const [showPolicy, setShowPolicy] = useState(false);
  const [showPassword ,setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    confirmEmail: "",
    password: "",
    confirmPassword: "",
    phone: "",
    country: "Brasil",
    state: "",
    agencyName: "",
    companySize: "",
    source: "",
    terms: false,
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  // 📞 FORMATAÇÃO TELEFONE
  const formatPhone = (value: string) => {
    if (!value) return "";
    const phoneNumber = value.replace(/\D/g, ""); // Remove letras
    const phoneLength = phoneNumber.length;

    if (phoneLength < 3) return phoneNumber;
    if (phoneLength < 7) return `(${phoneNumber.slice(0, 2)}) ${phoneNumber.slice(2)}`;
    return `(${phoneNumber.slice(0, 2)}) ${phoneNumber.slice(2, 7)}-${phoneNumber.slice(7, 11)}`;
  };

  const handleAcceptTerms = () => {
    // Atualiza o formData simulando um evento ou alterando o estado diretamente
    setFormData(prev => ({ ...prev, terms: true }));
    setShowTerms(false); 
    setShowPolicy(false); 
  };

  // 🔄 HANDLE CHANGE
  const handleChange = (e: any) => {
    const { name, value, type } = e.target;

    const val = type === "checkbox" ? e.target.checked : value;
    const finalValue = name === "phone" ? formatPhone(value) : val;

    setFormData((prev) => ({
      ...prev,
      [name]: finalValue,
    }));

    if (error) setError("");
  };

  // 📧 VALIDAÇÃO EMAIL
  const isValidEmail = (email: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  // 🔐 VALIDAÇÃO SENHA
  const isStrongPassword = (password: string) => {
    // Explicação da Regex:
    // (?=.*[A-Z])  -> Pelo menos uma letra maiúscula
    // (?=.*\d)     -> Pelo menos um número (Dígito)
    // (?=.*[\W_])  -> Pelo menos um símbolo (caractere especial ou underline)
    // .{8,}        -> No mínimo 8 caracteres
    return /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(password);
  };

  // 🚀 REGISTER
 

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();

    const email = formData.email.trim().toLowerCase();
    const confirmEmail = formData.confirmEmail.trim().toLowerCase();

    const isValidPhone = (phone: string) => {
      const digits = phone.replace(/\D/g, "");
      return digits.length === 11;
    };

    if (!isValidEmail(email)) {
      setError("Digite um e-mail válido.");
      return;
    }

    if (email !== confirmEmail) {
      setError("Os e-mails não coincidem.");
      return;
    }

    if (!isValidPhone(formData.phone)) {
      setError("Certifique-se de incluir o DDD e os 9 dígitos do seu número.");
      return;
    }

    if (!isStrongPassword(formData.password)) {
      setError("A senha deve ter pelo menos 8 caracteres, incluindo maiúscula, número e símbolo.");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("As senhas não coincidem.");
      return;
    }

    if (!formData.companySize) {
      setError("Selecione o tamanho da equipe.");
      return;
    }

    if (!formData.source) {
      setError("Informe como conheceu a plataforma.");
      return;
    }

    if (!formData.terms) {
      setError("Aceite os termos e política.");
      return;
    }

    setLoading(true);

    try {
      const payload = {
        name: formData.name,
        email,
        password: formData.password,
        phone: formData.phone,
        country: formData.country,
        state: formData.state,
        agency_name: formData.agencyName,
        company_size: formData.companySize,
        source: formData.source,
      };

      const res = await axios.post("http://localhost:8000/auth/register", payload);

      // 🔐 salva token (SE você ajustar backend pra retornar token)
      if (res.data.access_token) {
        localStorage.setItem("token", res.data.access_token);
        document.cookie = `token=${res.data.access_token}; path=/`;
        router.push("/dashboard");
      } else {
        router.push("/login");
      }

    } catch (err: any) {
      console.error(err);

      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Erro ao criar conta.");
      }
    } finally {
      setLoading(false);
    }
  }

  // 🌐 SOCIAL LOGIN
  const handleOAuth = (provider: string) => {
    window.location.href = `http://localhost:8000/auth/${provider}`;
  };

  if (!mounted) return null;

  return (
    <div className="flex items-center justify-center min-h-screen bg-brand-dark p-4 md:p-10 py-20">
      <div className="w-full max-w-[700px]">

        {/* VOLTAR */}
        <Link href="/" className="inline-flex items-center gap-2 text-brand-muted mb-6 text-xs font-bold">
          <ArrowLeft size={14} /> Voltar
        </Link>

        <div className="bg-brand-surface p-8 md:p-12 rounded-[2.5rem] border border-brand-border shadow-2xl">

          {/* LOGO */}
          <div className="flex flex-col items-center mb-10">
            <div className="bg-brand-primary p-4 rounded-2xl mb-4">
              <Rocket size={32} className="text-white" />
            </div>
            <h2 className="text-3xl font-black text-white">
              InsightFlow
            </h2>
          </div>

          {/* 🔥 SOCIAL LOGIN */}
          <p className="text-center text-brand-muted text-xs mb-4 uppercase tracking-widest font-medium">
            Cadastre-se rapidamente
          </p>

          {/* Aqui vêm os seus botões do Google, Microsoft e Apple */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8">
            <button onClick={() => handleOAuth("google")} className="flex items-center justify-center gap-4 bg-white hover:bg-gray-200 text-black p-3 rounded-xl font-bold text-xs transition-colors duration-200 border border-transparent hover:border-gray-200 duration-500 ease-in-out shadow-sm">
              <FcGoogle size={24} color="red" />
              <span>Google</span> 
            </button>
            <button onClick={() => handleOAuth("microsoft")} className="flex items-center justify-center gap-4 bg-white hover:bg-gray-200 text-black p-3 rounded-xl font-bold text-xs transition-colors duration-200 border border-transparent hover:border-gray-200 duration-500 ease-in-out shadow-sm">
              <FaMicrosoft size={20} className="text-blue-500" />
              <span>Microsoft</span> 
            </button>
            <button onClick={() => handleOAuth("apple")} className="flex items-center justify-center gap-4 bg-white hover:bg-gray-200 text-black p-3 rounded-xl font-bold text-xs transition-colors duration-200 border border-transparent hover:border-gray-200 duration-500 ease-in-out shadow-sm">
              <FaApple size={20} className="text-black group-hover:text-black transition-colors" />
              <span>Apple</span> 
            </button>
          </div>
          
          {/* Divisor Visual */}
          <div className="relative flex items-center justify-center my-10">
            {/* Linha da esquerda */}
            <div className="flex-grow border-t border-brand-border/50"></div>
            
            {/* Texto Central */}
            <span className="flex-shrink mx-4 text-brand-muted text-[10px] uppercase font-bold tracking-[0.2em]">
              Ou continue com e-mail
            </span>
            
            {/* Linha da direita */}
            <div className="flex-grow border-t border-brand-border/50"></div>
          </div>
 
          {/* ERRO */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500 text-sm flex gap-2">
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <form onSubmit={handleRegister} className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <input name="name" placeholder="Nome completo" onChange={handleChange} value={formData.name} required className="md:col-span-2 p-4 rounded-xl bg-brand-dark text-white" />

            <input name="email" placeholder="Email" onChange={handleChange} value={formData.email} required className="p-4 rounded-xl bg-brand-dark text-white" />
            <input name="confirmEmail" placeholder="Confirmar Email" onChange={handleChange} value={formData.confirmEmail} required className="p-4 rounded-xl bg-brand-dark text-white" />

            <input name="phone" placeholder="(00) 00000-0000" onChange={handleChange} value={formData.phone} required className="p-4 rounded-xl bg-brand-dark text-white" />

            <select name="country" onChange={handleChange} value={formData.country} className="p-4 rounded-xl bg-brand-dark text-white">
              <option>Brasil</option>
              <option>Portugal</option>
              <option>USA</option>
            </select>

            <input name="state" placeholder="Estado" onChange={handleChange} value={formData.state} required className="p-4 rounded-xl bg-brand-dark text-white" />

            <input name="agencyName" placeholder="Nome da Agência" onChange={handleChange} value={formData.agencyName} required className="p-4 rounded-xl bg-brand-dark text-white" />

            <select name="companySize" onChange={handleChange} value={formData.companySize} required className="p-4 rounded-xl bg-brand-dark text-white">
              <option value="">Tamanho da equipe</option>
              <option value="solo">Solo</option>
              <option value="2-10">2-10</option>
              <option value="11-50">11-50</option>
              <option value="50+">50+</option>
            </select>

            <select name="source" onChange={handleChange} value={formData.source} required className="p-4 rounded-xl bg-brand-dark text-white">
              <option value="">Como conheceu</option>
              <option value="google">Google</option>
              <option value="instagram">Instagram</option>
              <option value="youtube">YouTube</option>
              <option value="indicacao">Indicação</option>
            </select>
            <div className="relative flex items-center w-full">
              <input 
                
                type={showPassword ? "text" : "password"} 
                name="password" 
                placeholder="Senha" 
                onChange={handleChange} 
                value={formData.password} 
                required 
                
                className="w-full p-4 pr-12 rounded-xl bg-brand-dark text-white border border-brand-border focus:border-brand-primary outline-none transition-all" 
              />
              
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 text-brand-muted hover:text-brand-primary transition-colors"
                aria-label={showPassword ? "Esconder senha" : "Mostrar senha"}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>

            <div className="relative flex items-center w-full">
              <input 
                type={showConfirmPassword ? "text" : "password"} 
                name="confirmPassword" 
                placeholder="Confirmar senha" 
                onChange={handleChange} 
                value={formData.confirmPassword} 
                required 
                className="w-full p-4 pr-12 rounded-xl bg-brand-dark text-white border border-brand-border focus:border-brand-primary outline-none transition-all" 
              />
              
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-4 text-brand-muted hover:text-brand-primary transition-colors"
              >
                {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>


            <div className="flex items-center md:col-span-2 flex items-start gap-3 text-sm text-brand-muted group">
              {/* Checkbox Customizado */}
              <div className="relative flex items-center mt-1 gap-2">
                <input
                  id="terms"
                  name="terms"
                  type="checkbox"
                  checked={formData.terms}
                  onChange={handleChange}
                  className="peer h-5 w-5 cursor-pointer appearance-none rounded-md border-2 border-brand-border bg-brand-dark checked:bg-brand-primary checked:border-brand-primary transition-all duration-200 hover:border-brand-primary/50"
                />
                {/* Ícone de Check (Só aparece quando marcado) */}
                <svg
                  className="absolute h-3.5 w-3.5 text-white opacity-0 peer-checked:opacity-100 pointer-events-none top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 transition-opacity"
                  xmlns="http://www.w3.org"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="4"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              </div>
                
              <label htmlFor="terms" className="text-[11px] text-brand-muted leading-relaxed font-medium">
                Aceito os{" "}
                <button 
                  type="button" 
                  onClick={() => setShowTerms(true)} 
                  className="text-brand-primary underline hover:text-white transition-colors"
                >
                  Termos de Uso
                </button>
                {" "}e concordo com a{" "}
                <button 
                  type="button" 
                  onClick={() => setShowPolicy(true)} 
                  className="text-brand-primary underline hover:text-white transition-colors"
                >
                  Política de Privacidade
                </button>.
              </label>
          </div>

            <button disabled={loading} className="md:col-span-2 bg-brand-primary py-5 rounded-xl text-white font-bold">
              {loading ? "Criando..." : "Criar Conta"}
            </button>

          </form>

          <p className="mt-8 text-center text-brand-muted text-sm">
            Já tem conta? <Link href="/login" className="text-brand-primary font-bold">Login</Link>
          </p>

        </div>
      </div>
      {/* MODAL DE TERMOS */}
      <TermsModal 
        isOpen={showTerms} 
        onClose={handleAcceptTerms} 
      />

      {/* MODAL DE POLÍTICA */}
      <PolicyModal 
        isOpen={showPolicy} 
        onClose={handleAcceptTerms} 
      />
      
    </div>
  );
}