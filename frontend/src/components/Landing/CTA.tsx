import Link from "next/link";

export default function CTA() {
  return (
    <section className="text-center py-20">
      <h2 className="text-2xl font-bold mb-4">
        Pronto para melhorar seus resultados?
      </h2>

      <Link
        href="/register"
        className="bg-brand-primary px-8 py-3 rounded-md text-white"
      >
        Criar conta grátis
      </Link>
    </section>
  );
}