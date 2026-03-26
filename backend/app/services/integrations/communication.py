from datetime import date
import random


def generate_communication_data():
    return [
        {
            "channel": "email",
            "sent": random.randint(100, 500),
            "opened": random.randint(50, 300),
            "clicked": random.randint(10, 100),
            "date": date.today()
        },
        {
            "channel": "whatsapp",
            "sent": random.randint(50, 200),
            "opened": random.randint(40, 180),
            "clicked": random.randint(5, 80),
            "date": date.today()
        }
    ]