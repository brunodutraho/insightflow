from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.subscription import Subscription
from app.models.plan import Plan


def migrate_subscriptions():
    db: Session = SessionLocal()

    subs = db.query(Subscription).all()

    for sub in subs:
        if sub.plan_id:
            continue

        plan = db.query(Plan).filter(Plan.name == sub.plan).first()

        if plan:
            sub.plan_id = plan.id

    db.commit()
    db.close()


if __name__ == "__main__":
    migrate_subscriptions()