from app.services.integrations.base import BaseIntegration
from datetime import date
import random


class TikTokIntegration(BaseIntegration):

    def fetch_data(self):
        return [
            {
                "impressions": random.randint(500, 3000),
                "clicks": random.randint(20, 150),
                "spend": round(random.uniform(30, 200), 2),
                "conversions": random.randint(0, 10),
                "date": date.today()
            }
        ]

    def transform(self, raw_data):
        result = []

        for r in raw_data:
            result.append({
                "platform": "tiktok",
                **r
            })

        return result