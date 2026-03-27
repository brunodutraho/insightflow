import { Rocket } from "lucide-react";
import Link from "next/link"; // 1. Importe o Link

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-slate-950 text-white">
      <Rocket className="text-blue-500 w-12 h-12 mb-4" />
      <h1 className="text-4xl font-bold">InsightFlow</h1>
      <p className="mt-2 text-slate-400">O motor de dados está pronto. Bem-vindo ao Front-end profissional do seu SaaS.</p>
      <Link href="/dashboard">
        <button className="mt-8 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg transition-all">
          Ir para Dashboard
        </button>
      </Link>
    </main>
  );
}

