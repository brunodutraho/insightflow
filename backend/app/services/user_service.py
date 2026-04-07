from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User
from app.models.subscription import Subscription
from app.auth.utils import hash_password


# ================================
# HEALTH SCORE (REGRA CENTRAL)
# ================================
def calculate_health(last_login: datetime | None):
    if not last_login:
        return "critical"

    days = (datetime.utcnow() - last_login).days

    if days > 14:
        return "critical"
    elif days > 7:
        return "warning"
    else:
        return "healthy"


# ================================
# LISTAGEM ADMIN (CORE)
# ================================
def get_users_admin(
    db: Session,
    role: str | None = None,
    status: str | None = None,
    search: str | None = None
):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if search:
        query = query.filter(User.email.ilike(f"%{search}%"))

    users = query.all()

    result = []

    for user in users:
        health = calculate_health(user.last_login)

        if status and health != status:
            continue

        last_login_days = (
            (datetime.utcnow() - user.last_login).days
            if user.last_login else None
        )

        result.append({
            "id": user.id,
            "email": user.email,
            "role": user.role,

            # 🔥 CORREÇÃO AQUI
            "is_internal": user.role in ["admin", "staff"],

            "is_blocked": getattr(user, "is_blocked", False),

            "last_login_days": last_login_days,
            "health_status": health
        })

    return result


# ================================
# RESET DE SENHA
# ================================
def reset_user_password(db: Session, user_id: int, new_pwd: str):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception("Usuário não encontrado")

    user.hashed_password = hash_password(new_pwd)

    if hasattr(user, "require_password_change"):
        user.require_password_change = True

    db.commit()
    return True


# ================================
# BONUS DE ACESSO
# ================================
def grant_bonus_days(db: Session, user_id: int, days: int):
    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    if sub:
        base_date = (
            sub.expires_at
            if sub.expires_at and sub.expires_at > datetime.utcnow()
            else datetime.utcnow()
        )
        sub.expires_at = base_date + timedelta(days=days)

    else:
        user = db.query(User).filter(User.id == user_id).first()

        if hasattr(user, "access_expires_at"):
            base_date = (
                user.access_expires_at
                if user.access_expires_at and user.access_expires_at > datetime.utcnow()
                else datetime.utcnow()
            )
            user.access_expires_at = base_date + timedelta(days=days)

    db.commit()
    return True


# ================================
# BLOQUEAR / DESBLOQUEAR
# ================================
def toggle_block_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception("Usuário não encontrado")

    user.is_blocked = not getattr(user, "is_blocked", False)

    db.commit()
    return user.is_blocked



def count_users(db, tenant_id):
    return db.query(User).filter(
        User.tenant_id == tenant_id
    ).count()