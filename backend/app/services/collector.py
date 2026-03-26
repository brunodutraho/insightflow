from app.database.database import SessionLocal

from app.models.marketing_metric import MarketingMetric
from app.models.communication_metric import CommunicationMetric

from app.services.integrations.google_ads import GoogleAdsIntegration
from app.services.integrations.tiktok_ads import TikTokIntegration
from app.services.integrations.meta_ads import MetaAdsIntegration
from app.services.integrations.linkedin_ads import LinkedInIntegration
from app.services.integrations.communication import generate_communication_data


def run_collector():
    db = SessionLocal()

    try:
        integrations = [
            GoogleAdsIntegration(),
            TikTokIntegration(),
            MetaAdsIntegration(),
            LinkedInIntegration()
        ]

        # coleta ads
        for integration in integrations:
            raw = integration.fetch_data()
            data = integration.transform(raw)

            for d in data:
                metric = MarketingMetric(
                    client_id=1,
                    platform=d["platform"],
                    impressions=d["impressions"],
                    clicks=d["clicks"],
                    spend=d["spend"],
                    conversions=d["conversions"],
                    date=d["date"]
                )

                db.add(metric)

        # comunicação (email / whatsapp)
        comm_data = generate_communication_data()

        for c in comm_data:
            metric = CommunicationMetric(
                client_id=1,
                channel=c["channel"],
                sent=c["sent"],
                opened=c["opened"],
                clicked=c["clicked"],
                date=c["date"]
            )

            db.add(metric)

        db.commit()
        print("✅ Data collection completed")

    except Exception as e:
        db.rollback()
        print("❌ Error during collection:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_collector()