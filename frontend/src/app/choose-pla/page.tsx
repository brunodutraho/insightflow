"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";

export default function ChoosePlanPage() {
  const [plans, setPlans] = useState([]);

  useEffect(() => {
    async function fetchPlans() {
      const res = await api.get("/plans");
      setPlans(res.data);
    }

    fetchPlans();
  }, []);

  async function handleSelect(planId: string) {
    const res = await api.post("/billing/checkout", {
      plan_id: planId
    });

    window.location.href = res.data.checkout_url;
  }

  return (
    <div className="min-h-screen bg-slate-950 flex justify-center items-center p-10">
      <div className="grid md:grid-cols-3 gap-6">

        {plans.map((plan: any) => (
          <div key={plan.id} className="bg-slate-900 p-6 rounded-2xl border border-slate-800">
            
            <h3 className="text-xl text-white font-bold">{plan.name}</h3>
            <p className="text-slate-400 text-sm mb-4">{plan.description}</p>

            <p className="text-2xl text-blue-500 font-bold mb-6">
              R$ {plan.price}
            </p>

            <button
              onClick={() => handleSelect(plan.id)}
              className="w-full py-3 bg-blue-600 rounded-xl text-white"
            >
              Escolher plano
            </button>

          </div>
        ))}

      </div>
    </div>
  );
}