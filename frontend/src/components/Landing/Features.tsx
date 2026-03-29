export default function Features() {
  return (
    <section className="py-20 px-8 grid md:grid-cols-3 gap-8">
      <div className="bg-brand-surface p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">KPIs centralizados</h3>
        <p className="text-brand-muted">
          Visualize métricas de todas as plataformas em um único lugar.
        </p>
      </div>

      <div className="bg-brand-surface p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Score de performance</h3>
        <p className="text-brand-muted">
          Avalie rapidamente a saúde das suas campanhas com um score inteligente.
        </p>
      </div>

      <div className="bg-brand-surface p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Insights automáticos</h3>
        <p className="text-brand-muted">
          Receba recomendações acionáveis para melhorar resultados.
        </p>
      </div>
    </section>
  );
}