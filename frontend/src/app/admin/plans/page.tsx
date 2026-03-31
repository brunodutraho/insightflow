"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import ReauthModal from "@/components/dashboard/ReauthModal";

type Plan = {
  id: number;
  name: string;
  price: number;
  max_clients: number;
  is_active: boolean;
};

export default function PlansPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<Plan | null>(null);
  const [showModal, setShowModal] = useState(false);

  async function fetchPlans() {
    const res = await api.get("/admin/plans");
    setPlans(res.data);
  }

  useEffect(() => {
    fetchPlans();
  }, []);

  // 🔥 abre modal
  function requestUpdate(plan: Plan) {
    setSelectedPlan(plan);
    setShowModal(true);
  }

  // 🔐 só salva depois de confirmar senha
  async function confirmUpdate() {
    if (!selectedPlan) return;

    await api.put(`/admin/plans/${selectedPlan.id}`, selectedPlan);

    setShowModal(false);
    fetchPlans();
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Planos</h1>

      {plans.map((plan) => (
        <div
          key={plan.id}
          className="border p-4 rounded-lg flex flex-col gap-2"
        >
          <input
            value={plan.name}
            onChange={(e) =>
              setPlans((prev) =>
                prev.map((p) =>
                  p.id === plan.id ? { ...p, name: e.target.value } : p
                )
              )
            }
          />

          <input
            type="number"
            value={plan.price}
            onChange={(e) =>
              setPlans((prev) =>
                prev.map((p) =>
                  p.id === plan.id
                    ? { ...p, price: Number(e.target.value) }
                    : p
                )
              )
            }
          />

          <button
            onClick={() => requestUpdate(plan)} // 🔥 AQUI FOI A MUDANÇA
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Salvar
          </button>
        </div>
      ))}

      {/* 🔐 MODAL */}
      {showModal && (
        <ReauthModal
          onClose={() => setShowModal(false)}
          onSuccess={confirmUpdate}
        />
      )}
    </div>
  );
}