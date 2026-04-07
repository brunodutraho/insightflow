"use client"

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function OAuthSuccess() {
  const router = useRouter();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (token) {
      localStorage.setItem("token", token);
      router.push("/choose-plan");
    } else {
      router.push("/login");
    }
  }, []);

  return <p>Autenticando...</p>;
}