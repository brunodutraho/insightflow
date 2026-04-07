"use client";

import { useState, useEffect } from "react";
import api from "@/services/api";

interface MRRGoalCardProps {
  current: number;
  goal: {
    target: number;
    expected_progress: number;
  };
  onUpdate: () => void;
}

export function MRRGoalCard({ current, goal, onUpdate }: MRRGoalCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [password, setPassword] = useState("");
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error', msg: string } | null>(null);
  
  const [displayValue, setDisplayValue] = useState("");
  const [numericValue, setNumericValue] = useState(0);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
  };

  // Sincroniza o valor inicial vindo do banco
  useEffect(() => {
    if (goal?.target !== undefined) {
      setNumericValue(goal.target);
      setDisplayValue(formatCurrency(goal.target));
    }
  }, [goal?.target]);

  const target = goal?.target || 0;
  const expected = goal?.expected_progress || 0;
  const progress = target > 0 ? (current / target) * 100 : 0;
  const isOnTrack = progress >= expected;

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value.replace(/\D/g, ""); 
    
    if (!value || value === "0") {
      setNumericValue(0);
      setDisplayValue("");
      return;
    }

    // Lógica para R$ 0,00 (centavos)
    const numberValue = Number(value) / 100;
    setNumericValue(numberValue);
    setDisplayValue(formatCurrency(numberValue));
  };

  // Função crucial: Limpa tudo e avisa o pai para recarregar
  const handleCloseSuccess = () => {
    setFeedback(null);
    setIsEditing(false);
    setPassword("");
    onUpdate(); 
  };

  const handleSave = async () => {
    if (!password) {
      setFeedback({ type: 'error', msg: "Senha de administrador obrigatória." });
      return;
    }

    try {
      setLoading(true);
      // Enviando o valor numérico limpo
      const response = await api.post("/admin/goal/mrr", { 
        target: parseFloat(numericValue.toFixed(2)), 
        password: password 
      });
      
      if (response.status === 200 || response.status === 201) {
        setFeedback({ 
          type: 'success', 
          msg: "A nova meta de faturamento foi salva com sucesso no sistema." 
        });
      }
    } catch (err: any) {
      setFeedback({ 
        type: 'error', 
        msg: err.response?.data?.detail || "Erro ao validar senha ou salvar meta." 
      });
    } finally {
      setLoading(false);
    }
  };

  if (!goal) return <div className="h-48 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-2xl" />;

  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-2xl shadow-sm relative group">
      
      {/* MODAL DE FEEDBACK */}
      {feedback && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/60 backdrop-blur-sm px-4">
          <div className="bg-white dark:bg-slate-900 p-8 rounded-[2rem] shadow-2xl border border-slate-200 dark:border-slate-800 max-w-sm w-full animate-in zoom-in-95 duration-300">
            <div className="text-center">
              <div className={`text-6xl mb-4 ${feedback.type === 'success' ? 'text-emerald-500' : 'text-rose-500'}`}>
                {feedback.type === 'success' ? '🚀' : '🔒'}
              </div>
              <h3 className="text-xl font-black text-slate-900 dark:text-white mb-2 uppercase">
                {feedback.type === 'success' ? 'Meta Atualizada!' : 'Acesso Negado'}
              </h3>
              <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-8 leading-relaxed">
                {feedback.msg}
              </p>
              
              <button 
                onClick={feedback.type === 'success' ? handleCloseSuccess : () => setFeedback(null)}
                className={`w-full py-4 rounded-2xl font-black text-sm uppercase tracking-widest transition-all active:scale-95 ${
                  feedback.type === 'success' 
                  ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30' 
                  : 'bg-slate-900 dark:bg-white text-white dark:text-slate-900'
                }`}
              >
                {feedback.type === 'success' ? 'Entendido' : 'Tentar Novamente'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* HEADER DO CARD */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-[10px] font-black uppercase tracking-[0.2em] text-purple-600 dark:text-purple-400">
          🎯 Ritmo da Meta
        </h2>

        {!isEditing ? (
          <button 
            onClick={() => setIsEditing(true)}
            className="text-[10px] bg-slate-100 dark:bg-slate-800 hover:bg-purple-600 hover:text-white px-4 py-2 rounded-xl font-black transition-all opacity-0 group-hover:opacity-100"
          >
            EDITAR META
          </button>
        ) : (
          <div className="flex gap-2">
            <button 
              onClick={handleSave} 
              disabled={loading}
              className="text-[10px] bg-purple-600 text-white px-4 py-2 rounded-xl font-black hover:bg-purple-700 disabled:opacity-50"
            >
              {loading ? "PROCESSANDO..." : "CONFIRMAR"}
            </button>
            <button 
              onClick={() => { setIsEditing(false); setPassword(""); }} 
              className="text-[10px] bg-slate-200 dark:bg-slate-700 px-4 py-2 rounded-xl font-black"
            >
              CANCELAR
            </button>
          </div>
        )}
      </div>

      {/* VALORES */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div>
          <p className="text-[10px] text-slate-400 uppercase font-black mb-1 tracking-tighter">Faturamento Atual</p>
          <p className="text-2xl font-black text-slate-800 dark:text-slate-100 italic">
            {formatCurrency(current)}
          </p>
        </div>

        <div className="md:text-right">
          <p className="text-[10px] text-slate-400 uppercase font-black mb-1 tracking-tighter">Meta Objetivo</p>
          {isEditing ? (
            <div className="flex flex-col items-end gap-3">
              <input 
                type="text" 
                className="w-full md:w-56 text-right bg-purple-50 dark:bg-purple-900/20 border-2 border-purple-200 dark:border-purple-800 rounded-2xl font-black text-xl outline-none px-4 py-2 text-purple-600"
                value={displayValue}
                onChange={handleInputChange}
                placeholder="R$ 0,00"
                autoFocus
              />
              <input 
                type="password" 
                className="w-full md:w-40 text-right bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-xs px-3 py-2 outline-none"
                placeholder="Senha de Admin"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          ) : (
            <p className="text-2xl font-black text-slate-300 dark:text-slate-600 tracking-tighter">
              {formatCurrency(target)}
            </p>
          )}
        </div>
      </div>

      {/* BARRA DE PROGRESSO */}
      <div className="relative w-full h-6 bg-slate-100 dark:bg-slate-800 rounded-2xl mb-4 overflow-hidden border border-slate-200 dark:border-slate-800">
        <div
          className={`h-full transition-all duration-1000 ease-out ${
            isOnTrack ? 'bg-gradient-to-r from-purple-600 to-indigo-500' : 'bg-rose-500'
          }`}
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
        {/* Marcador de Ritmo Esperado */}
        <div 
          className="absolute top-0 h-full w-1 bg-slate-900 dark:bg-white z-10 shadow-[0_0_10px_rgba(0,0,0,0.5)]"
          style={{ left: `${expected}%` }}
        />
      </div>

      <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-tight bg-slate-50 dark:bg-slate-800/50 p-3 rounded-2xl border border-slate-100 dark:border-slate-800">
        <span className={isOnTrack ? "text-emerald-500" : "text-rose-500"}>
          {isOnTrack ? "🚀 Acima do ritmo" : "⚠️ Abaixo do ritmo esperado"}
        </span>
        <span className="text-slate-500">
          {progress.toFixed(1)}% da meta batida
        </span>
      </div>
    </div>
  );
}
