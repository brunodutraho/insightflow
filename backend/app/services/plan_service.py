from sqlalchemy.orm import Session
from app.models.plan import Plan


def get_all_plans(db: Session):
    return db.query(Plan).order_by(Plan.price).all()


def update_plan(db: Session, plan_id: int, data: dict):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        return None

    if "name" in data:
        plan.name = data["name"]

    if "price" in data:
        plan.price = data["price"]

    if "max_clients" in data:
        plan.max_clients = data["max_clients"]

    if "is_active" in data:
        plan.is_active = data["is_active"]

    db.commit()
    db.refresh(plan)

    return plan


def create_plan(db: Session, data: dict):
    plan = Plan(**data)

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan