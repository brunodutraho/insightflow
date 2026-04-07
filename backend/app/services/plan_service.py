from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.models.subscription import Subscription


# =============================
# PLAN CRUD
# =============================

def get_all_plans(db: Session):
    return db.query(Plan).order_by(Plan.price).all()


def get_plan_by_id(db: Session, plan_id):
    return db.query(Plan).filter(Plan.id == plan_id).first()


def create_plan(db: Session, data: dict):
    plan = Plan(**data)

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def update_plan(db: Session, plan_id, data: dict):
    plan = get_plan_by_id(db, plan_id)

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


def delete_plan(db: Session, plan_id):
    plan = get_plan_by_id(db, plan_id)

    if not plan:
        return False

    db.delete(plan)
    db.commit()

    return True


# =============================
# SUBSCRIPTION LOGIC
# =============================

def get_active_subscription(db: Session, tenant_id):
    return db.query(Subscription).filter(
        Subscription.tenant_id == tenant_id,
        Subscription.is_active == True
    ).first()


# =============================
# FEATURE FLAG SYSTEM
# =============================

def has_feature(db: Session, tenant_id, feature_code: str) -> bool:
    """
    Verifica se o tenant possui acesso a uma feature específica
    """

    subscription = get_active_subscription(db, tenant_id)

    if not subscription:
        return False

    # evita erro caso não venha carregado
    if not subscription.plan or not subscription.plan.plan_features:
        return False

    for plan_feature in subscription.plan.plan_features:
        if (
            plan_feature.feature
            and plan_feature.feature.code == feature_code
            and plan_feature.enabled
        ):
            return True

    return False