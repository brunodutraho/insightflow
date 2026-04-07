from app.database.database import SessionLocal

from app.models.marketing_metric import MarketingMetric
from app.models.communication_metric import CommunicationMetric
from app.models.client import Tenant  

from app.services.integrations.google_ads import GoogleAdsIntegration
from app.services.integrations.tiktok_ads import TikTokIntegration
from app.services.integrations.meta_ads import MetaAdsIntegration
from app.services.integrations.linkedin_ads import LinkedInIntegration
from app.services.integrations.communication import generate_communication_data

def run_collector():
    db = SessionLocal()

    try:
        # BUSCA TODOS OS CLIENTES (TENANTS)
        clients = db.query(Tenant).all()

        if not clients:
            print("⚠️ Nenhum cliente encontrado. Pulando coleta.")
            return

        integrations = [
            GoogleAdsIntegration(),
            TikTokIntegration(),
            MetaAdsIntegration(),
            LinkedInIntegration()
        ]

        # LOOP POR CLIENTE (TENANT)
        for client in clients:
            # Pegamos o ID do tenant para vincular as métricas
            current_tenant_id = client.id

            # =========================
            # MARKETING METRICS
            # =========================
            for integration in integrations:
                raw = integration.fetch_data()
                data = integration.transform(raw)

                for d in data:
                    # CORRIGIDO: de client_id= para tenant_id=
                    metric = MarketingMetric(
                        tenant_id=current_tenant_id, 
                        platform=d["platform"],
                        impressions=d["impressions"],
                        clicks=d["clicks"],
                        spend=d["spend"],
                        conversions=d["conversions"],
                        date=d["date"]
                    )
                    db.add(metric)

            # =========================
            # COMMUNICATION METRICS
            # =========================
            comm_data = generate_communication_data()

            for c in comm_data:
                # CORRIGIDO: de client_id= para tenant_id=
                metric = CommunicationMetric(
                    tenant_id=current_tenant_id,
                    channel=c["channel"],
                    sent=c["sent"],
                    opened=c["opened"],
                    clicked=c["clicked"],
                    date=c["date"]
                )
                db.add(metric)

        db.commit()
        print(f"✅ Coleta finalizada para {len(clients)} clientes.")

    except Exception as e:
        db.rollback()
        print("❌ Erro durante a coleta:", e)

    finally:
        db.close()

if __name__ == "__main__":
    run_collector()
