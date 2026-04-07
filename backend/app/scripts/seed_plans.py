from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.plan import Plan


def seed_plans():
    db: Session = SessionLocal()

    plans = [
        {"name": "free", "price": 0, "max_clients": 1},
        {"name": "basic", "price": 49, "max_clients": 3},
        {"name": "pro", "price": 99, "max_clients": 10},
        {"name": "enterprise", "price": 199, "max_clients": 999},
    ]

    for p in plans:
        existing = db.query(Plan).filter(Plan.name == p["name"]).first()

        if not existing:
            plan = Plan(**p)
            db.add(plan)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_plans()