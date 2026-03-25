import app.models

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.ad_account import AdAccount
from app.models.ad_metric import AdMetric
from app.services.integrations.meta_ads import fetch_meta_ads_data


def run_collector():
    db: Session = SessionLocal()

    accounts = db.query(AdAccount).all()

    for account in accounts:
        if account.platform == "meta":
            data = fetch_meta_ads_data(account)

            metric = AdMetric(
                client_id=account.client_id,
                impressions=data["impressions"],
                clicks=data["clicks"],
                spend=data["spend"],
                date=data["date"]
            )

            db.add(metric)

    db.commit()
    db.close()


if __name__ == "__main__":
    run_collector()