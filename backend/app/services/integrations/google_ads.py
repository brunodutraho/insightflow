from app.services.integrations.base import BaseIntegration
from datetime import date
import random


class GoogleAdsIntegration(BaseIntegration):

    def fetch_data(self):
        # 🔥 dados fake simulando API
        return [
            {
                "impressions": random.randint(1000, 5000),
                "clicks": random.randint(50, 200),
                "spend": round(random.uniform(50, 300), 2),
                "conversions": random.randint(1, 20),
                "date": date.today()
            }
        ]

    def transform(self, raw_data):
        result = []

        for r in raw_data:
            result.append({
                "platform": "google",
                **r
            })

        return result