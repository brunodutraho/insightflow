"use client";

import { useSearchParams } from "next/navigation";
import VerifyEmailForm from "@/components/auth/VerifyEmailForm";

export default function VerifyEmailPage() {
  const params = useSearchParams();
  const email = params.get("email") || "";

  return (
    <div className="flex justify-center items-center min-h-screen bg-slate-950">
      <VerifyEmailForm email={email} />
    </div>
  );
}