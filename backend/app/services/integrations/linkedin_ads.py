from app.services.integrations.base import BaseIntegration
from datetime import date
import random


class LinkedInIntegration(BaseIntegration):

    def fetch_data(self):
        return [
            {
                "impressions": random.randint(800, 4000),
                "clicks": random.randint(30, 180),
                "spend": round(random.uniform(100, 500), 2),
                "conversions": random.randint(2, 15),
                "date": date.today()
            }
        ]

    def transform(self, raw_data):
        result = []

        for r in raw_data:
            result.append({
                "platform": "linkedin",
                **r
            })

        return result