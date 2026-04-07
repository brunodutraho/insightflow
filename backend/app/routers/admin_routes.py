from datetime import datetime, timedelta, timezone
import string
import random
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db

# Auth
from app.auth.utils import hash_password
from app.auth.dependencies import require_roles, get_current_user

# Models
from app.models.user import User, UserRole, UserStatus
from app.models.client import Tenant

# Schemas
from app.schemas.user_admin import (
    UserAdminResponse, UpdateEmailRequest, 
    ResetPasswordRequest, GrantDaysRequest, CreateStaffRequest
)

# Services
from app.services import user_service as user_service
from app.services import metrics_service as metrics
from app.services.plan_service import get_all_plans, update_plan, create_plan
from app.services.coupon_service import get_all_coupons, create_coupon, update_coupon

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    # ATUALIZADO: Apenas Master e Gerente acessam o painel administrativo
    dependencies=[Depends(require_roles([UserRole.admin_master, UserRole.gerente]))]
)

# =========================================================
# DASHBOARD & METRICS
# =========================================================

@router.get("/overview")
def get_admin_overview(db: Session = Depends(get_db)):
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
    role_counts = db.query(User.role, func.count(User.id)).group_by(User.role).all()


    recent_managers = db.query(User)\
        .filter(User.role == UserRole.gestor_assinante)\
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
    return db.query(Tenant).all()


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
    
@router.get("/funnel")
def get_funnel(db: Session = Depends(get_db)):
    return metrics.get_trial_to_paid_funnel(db)

@router.get("/insights")
def get_insights(db: Session = Depends(get_db)):
    return metrics.get_smart_insights(db)

# =========================================================
# USER MANAGEMENT (SECURITY, ACCESS & BONUS)
# =========================================================

@router.get("/users")
def list_admin_users(
    search: str = Query(None),
    role: str = Query(None),
    status: str = Query(None),
    filter_type: str = Query(None, alias="filter"), 
    db: Session = Depends(get_db)
):
    query = db.query(User)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.email.ilike(search_filter)) | 
            (User.full_name.ilike(search_filter))
        )

    if role:
        query = query.filter(User.role == role)

    if status:
        query = query.filter(User.status == status)

    if filter_type == "at_risk":
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        query = query.filter(User.last_login < seven_days_ago)
        
    return query.order_by(User.created_at.desc()).all()


@router.post("/users/{user_id}/reset-password")
def admin_reset_password(
    user_id: int, 
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Gera senha temporária e obriga troca no próximo login"""
   
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    # Gera senha aleatória de 8 caracteres
    temp_pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    user.hashed_password = hash_password(temp_pwd)
    user.require_password_change = True # Flag para o frontend forçar troca
    
    # Log de Auditoria
    metrics.log_admin_action(db, admin.id, user.id, "reset_password")
    db.commit()
    
    return {"temp_password": temp_pwd}


@router.post("/users/{user_id}/grant-access")
def admin_grant_access(
    user_id: int, 
    days: int = Body(..., embed=True), 
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Injeta dias de bônus na assinatura do usuário"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    # Calcula nova data (soma ao que resta ou a partir de hoje)
    base_date = user.access_expires_at if user.access_expires_at and user.access_expires_at > datetime.utcnow() else datetime.utcnow()
    user.access_expires_at = base_date + timedelta(days=days)
    
    metrics.log_admin_action(db, admin.id, user.id, f"grant_{days}_days_bonus")
    db.commit()
    
    return {"new_expiry": user.access_expires_at}


@router.patch("/users/{user_id}/block")
def admin_toggle_block(
    user_id: int, 
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Bloqueia ou desbloqueia acesso do usuário"""
    user = db.query(User).filter(User.id == user_id).first()
    user.is_blocked = not user.is_blocked
    
    action = "block" if user.is_blocked else "unblock"
    metrics.log_admin_action(db, admin.id, user.id, f"{action}_user")
    
    db.commit()
    return {"is_blocked": user.is_blocked}

# =========================================================
# USER MANAGEMENT (SECURITY, ACCESS & BONUS)
# =========================================================

@router.get("/users", response_model=List[UserAdminResponse])
def admin_list_users_unified(
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    filter_type: Optional[str] = Query(None, alias="filter"),
    db: Session = Depends(get_db)
):
    """
    Listagem Unificada: Suporta filtros de busca, cargo, status 
    e o filtro de risco (at_risk).
    """
    # Se for um filtro de risco simples (at_risk)
    if filter_type == "at_risk":
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        return db.query(User).filter(User.last_login < seven_days_ago).all()
    
    # Caso contrário, usa o serviço de busca detalhada
    return user_service.get_users_admin(db, role, status, search)


@router.post("/users/{user_id}/reset-password", name="admin_user_reset_password_secure")
def admin_perform_reset_password(
    user_id: str, # Alterado para str por causa do UUID
    payload: ResetPasswordRequest, 
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Reset de senha com validação da senha do Admin"""
    from app.auth.utils import verify_password
    if not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(401, "Senha do administrador incorreta")
    
    # Gera senha aleatória
    temp_pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user_service.reset_user_password(db, user_id, temp_pwd)
    
    metrics.log_admin_action(db, admin.id, user_id, "reset_password")
    return {"temp_password": temp_pwd}


@router.post("/users/{user_id}/grant-access", name="admin_user_grant_access_secure")
def admin_perform_grant_access(
    user_id: str, 
    payload: GrantDaysRequest, 
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Bonificação de dias com validação de senha do Admin"""
    from app.auth.utils import verify_password
    if not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(401, "Senha do administrador incorreta")
    
    user_service.grant_bonus_days(db, user_id, payload.days)
    metrics.log_admin_action(db, admin.id, user_id, f"bonus_{payload.days}_days")
    return {"message": "Bônus aplicado com sucesso"}


@router.patch("/users/{user_id}/block", name="admin_user_block_toggle")
def admin_perform_block_user(
    user_id: str, 
    payload: ResetPasswordRequest, # Usando schema que pede senha do admin
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Bloqueio/Desbloqueio manual com validação de senha do Admin"""
    from app.auth.utils import verify_password
    if not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(401, "Senha do administrador incorreta")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    # Inverte o status usando o Enum UserStatus que definimos
    if user.status == UserStatus.blocked:
        user.status = UserStatus.active
    else:
        user.status = UserStatus.blocked
        
    db.commit()
    metrics.log_admin_action(db, admin.id, user_id, "toggle_block")
    return {"status": user.status}
