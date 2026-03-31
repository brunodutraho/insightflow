from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.user import User, UserRole
from app.models.client import Client
from app.auth.dependencies import require_roles

# Services
from app.services import metrics_service as metrics
from app.services.plan_service import get_all_plans, update_plan, create_plan
from app.services.coupon_service import get_all_coupons, create_coupon, update_coupon
from fastapi import Body
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_roles(["admin"]))]
)

# =========================================================
# DASHBOARD & METRICS
# =========================================================

@router.get("/overview")
def get_admin_overview(db: Session = Depends(get_db)):
    """Rota principal consumida pelo componente React (AdminPage)"""
    return {
        "users": {
            "total": metrics.get_total_users(db),
            "new_last_30_days": metrics.get_new_users_30d(db),
            "growth_rate": metrics.get_users_growth_rate(db)
        },
        "revenue": {
            "active_subscriptions": metrics.get_active_subscriptions(db),
            "mrr": metrics.get_mrr(db),
            "arpu": metrics.get_arpu(db),
            "churn_rate": metrics.get_churn_rate(db),
            "mrr_growth": metrics.get_mrr_growth(db)
        },
        "goal": metrics.get_mrr_pacing(db)
    }


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    """Estatísticas detalhadas de distribuição de usuários"""
    role_counts = db.query(User.role, func.count(User.id)).group_by(User.role).all()

    recent_managers = db.query(User)\
        .filter(User.role == UserRole.gestor)\
        .order_by(User.created_at.desc())\
        .limit(5)\
        .all()

    return {
        "summary": {
            "total_users": metrics.get_total_users(db),
            "total_companies": metrics.get_total_companies(db)
        },
        "distribution": [
            {
                "role": r.value if hasattr(r, "value") else r,
                "count": c
            } for r, c in role_counts
        ],
        "recent_activity": [
            {
                "id": u.id,
                "email": u.email,
                "created_at": u.created_at
            } for u in recent_managers
        ]
    }


# =========================================================
# METRICS EXTENDED 
# =========================================================

@router.get("/mrr-history")
def get_admin_mrr_history(db: Session = Depends(get_db)):
    try:
        return metrics.get_mrr_history(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/at-risk-clients")
def read_at_risk(db: Session = Depends(get_db)):
    try:
        return metrics.get_at_risk_clients(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent-activity")
def get_recent_activity(db: Session = Depends(get_db)):
    """Timeline de eventos recentes"""
    try:
        return metrics.get_recent_activity(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar atividades recentes: {str(e)}"
        )


@router.get("/detailed-activity")
def get_detailed_activity(db: Session = Depends(get_db)):
    """Logs detalhados (cadastros + sessões)"""
    try:
        return metrics.get_detailed_activity(db)  # ✅ CORRIGIDO
    except Exception as e:
        print(f"Erro em detailed-activity: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar atividades detalhadas"
        )


# =========================================================
# MANAGEMENT (CLIENTS, PLANS, COUPONS)
# =========================================================

@router.get("/clients")
def list_all_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    return get_all_plans(db)


@router.post("/plans")
def create_new_plan(data: dict, db: Session = Depends(get_db)):
    return create_plan(db, data)


@router.put("/plans/{plan_id}")
def edit_plan(plan_id: int, data: dict, db: Session = Depends(get_db)):
    plan = update_plan(db, plan_id, data)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return plan


@router.get("/coupons")
def list_coupons(db: Session = Depends(get_db)):
    return get_all_coupons(db)


@router.post("/coupons")
def create_new_coupon(data: dict, db: Session = Depends(get_db)):
    if not data.get("code"):
        raise HTTPException(400, "Code required")

    if data.get("discount_percent") and data.get("discount_amount"):
        raise HTTPException(400, "Use either percent OR amount")

    return create_coupon(db, data)


@router.put("/coupons/{coupon_id}")
def edit_coupon(coupon_id: int, data: dict, db: Session = Depends(get_db)):
    return update_coupon(db, coupon_id, data)

@router.post("/goal/mrr")
def update_goal(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        return metrics.update_mrr_goal(
            db,
            user,
            new_goal=data.get("target"),
            password=data.get("password")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))