import Link from "next/link";

export default function Hero() {
  return (
    <section className="text-center py-24 px-6">
      <h1 className="text-4xl font-bold mb-6">
        Transforme dados em decisões inteligentes
      </h1>

      <p className="text-brand-muted max-w-xl mx-auto mb-8">
        Centralize métricas, visualize performance e receba insights automáticos
        para escalar seus resultados.
      </p>

      <div className="flex justify-center gap-4">
        <Link
          href="/register"
          className="bg-brand-primary px-6 py-3 rounded-md text-white"
        >
          Começar grátis
        </Link>

        <Link
          href="/login"
          className="border border-brand-border px-6 py-3 rounded-md"
        >
          Já tenho conta
        </Link>
        <div className="bg-brand-primary text-white p-6">
          COR FUNCIONANDO
        </div>
      </div>
    </section>
  );
}