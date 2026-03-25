import random
from datetime import date


def fetch_meta_ads_data(account):
    # data simulation
    return {
        "impressions": random.randint(1000, 5000),
        "clicks": random.randint(50, 300),
        "spend": round(random.uniform(10, 200), 2),
        "date": date.today()
    }