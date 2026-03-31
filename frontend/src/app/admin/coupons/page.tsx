"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";

type Coupon = {
  id: number;
  code: string;
  discount_percent?: number;
  discount_amount?: number;
  is_active: boolean;
};

export default function CouponsPage() {
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [newCode, setNewCode] = useState("");
  const [percent, setPercent] = useState<number | "">("");
  const [amount, setAmount] = useState<number | "">("");

  async function fetchCoupons() {
    const res = await api.get("/admin/coupons");
    setCoupons(res.data);
  }

  useEffect(() => {
    fetchCoupons();
  }, []);

  async function createCoupon() {
    await api.post("/admin/coupons", {
      code: newCode,
      discount_percent: percent || null,
      discount_amount: amount || null,
    });

    setNewCode("");
    setPercent("");
    setAmount("");

    fetchCoupons();
  }

  async function toggleCoupon(coupon: Coupon) {
    await api.put(`/admin/coupons/${coupon.id}`, {
      is_active: !coupon.is_active,
    });

    fetchCoupons();
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Cupons</h1>

      {/* CRIAR */}
      <div className="border p-4 rounded-lg space-y-2">
        <h2 className="font-semibold">Criar Cupom</h2>

        <input
          placeholder="Código (ex: WELCOME50)"
          value={newCode}
          onChange={(e) => setNewCode(e.target.value)}
          className="w-full p-2 border rounded"
        />

        <input
          type="number"
          placeholder="% desconto"
          value={percent}
          onChange={(e) => setPercent(Number(e.target.value))}
          className="w-full p-2 border rounded"
        />

        <input
          type="number"
          placeholder="Valor desconto (R$)"
          value={amount}
          onChange={(e) => setAmount(Number(e.target.value))}
          className="w-full p-2 border rounded"
        />

        <button
          onClick={createCoupon}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Criar
        </button>
      </div>

      {/* LISTA */}
      <div className="space-y-3">
        {coupons.map((c) => (
          <div
            key={c.id}
            className="border p-4 rounded-lg flex justify-between items-center"
          >
            <div>
              <p className="font-bold">{c.code}</p>

              {c.discount_percent && (
                <p>{c.discount_percent}% OFF</p>
              )}

              {c.discount_amount && (
                <p>R$ {c.discount_amount} OFF</p>
              )}
            </div>

            <button
              onClick={() => toggleCoupon(c)}
              className={`px-3 py-1 rounded text-sm ${
                c.is_active
                  ? "bg-green-500/20 text-green-600"
                  : "bg-gray-300 text-gray-600"
              }`}
            >
              {c.is_active ? "Ativo" : "Inativo"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}