from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

import calendar
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
from app.models.client import Client
from app.models.app_config import AppConfig
from app.auth.utils import verify_password
from app.models.activity import ActivityItem 


# =========================================================
# USERS
# =========================================================

def get_total_users(db: Session):
    return db.query(User).count()


def get_new_users_30d(db: Session):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    return db.query(User).filter(User.created_at >= thirty_days_ago).count()


def get_users_growth_rate(db: Session):
    now = datetime.utcnow()
    last_month = now - timedelta(days=30)
    prev_month = last_month - timedelta(days=30)

    current = db.query(User).filter(User.created_at >= last_month).count()
    previous = db.query(User).filter(
        User.created_at >= prev_month,
        User.created_at < last_month
    ).count()

    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


# =========================================================
# COMPANIES
# =========================================================

def get_total_companies(db: Session):
    return db.query(Client).count()


# =========================================================
# SUBSCRIPTIONS
# =========================================================

def get_active_subscriptions(db: Session):
    return db.query(Subscription).filter(Subscription.is_active == True).count()


def get_new_subscriptions_30d(db: Session):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    return db.query(Subscription).filter(
        Subscription.created_at >= thirty_days_ago
    ).count()


def get_canceled_subscriptions_30d(db: Session):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    return db.query(Subscription).filter(
        Subscription.canceled_at != None,
        Subscription.canceled_at >= thirty_days_ago
    ).count()


# =========================================================
# REVENUE
# =========================================================

def get_mrr(db: Session):
    result = db.query(func.sum(Plan.price))\
        .select_from(Subscription)\
        .join(Plan, Subscription.plan_id == Plan.id)\
        .filter(Subscription.is_active == True)\
        .scalar()

    return float(result or 0.0)


def get_mrr_growth(db: Session):
    now = datetime.utcnow()
    last_month = now - timedelta(days=30)
    prev_month = last_month - timedelta(days=30)

    current = db.query(func.sum(Plan.price))\
        .select_from(Subscription)\
        .join(Plan, Subscription.plan_id == Plan.id)\
        .filter(
            Subscription.created_at >= last_month,
            Subscription.is_active == True
        ).scalar() or 0

    previous = db.query(func.sum(Plan.price))\
        .select_from(Subscription)\
        .join(Plan, Subscription.plan_id == Plan.id)\
        .filter(
            Subscription.created_at >= prev_month,
            Subscription.created_at < last_month
        ).scalar() or 0

    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


def get_mrr_pacing(db: Session):
    """
    Lê a meta atualizada do banco e calcula o ritmo (pacing) do mês.
    Essa função é usada pelo GET /admin/overview para mostrar a barra.
    """
    # 1. Busca o valor que você salvou usando a função update_mrr_goal
    config = db.query(AppConfig).filter(AppConfig.key == "mrr_goal").first()
    
    # Se você ainda não salvou nada, ele assume 10000.0 como padrão
    target = float(config.value) if config and config.value else 10000.0

    # 2. Cálculo de Pacing (Ritmo do Calendário)
    now = datetime.now()
    # Retorna o último dia do mês atual (ex: 30 ou 31)
    _, total_days = calendar.monthrange(now.year, now.month)
    current_day = now.day

    # Calcula quanto % do mês já se passou até hoje
    expected_progress = (current_day / total_days) * 100

    return {
        "target": target,
        "expected_progress": round(expected_progress, 1)
    }


def update_mrr_goal(db: Session, user: User, new_goal: float, password: str):
    # 1. Valida a senha (IMPORTANTE: verify_password deve estar importado)
    if not verify_password(password, user.hashed_password):
        raise Exception("Senha inválida")

    # 2. Atualiza ou cria a meta no AppConfig
    config = db.query(AppConfig).filter(AppConfig.key == "mrr_goal").first()

    if not config:
        config = AppConfig(key="mrr_goal", value=new_goal)
        db.add(config)
    else:
        config.value = new_goal

    # 3. Registra a atividade para aparecer no componente de scroll (Timeline)
    try:
        nova_atividade = ActivityItem(
            type="configuracao",
            message=f"Meta de MRR alterada para R$ {new_goal:,.2f} por {user.email}",
            created_at=datetime.utcnow()
        )
        db.add(nova_atividade)
        
        # Faz o commit de tudo (Meta + Atividade)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao salvar atividade: {e}")
        # Mesmo que a atividade falhe, a meta já estaria salva se fizéssemos separado, 
        # mas aqui garantimos que ou salva os dois ou nenhum.
        raise Exception("Erro ao persistir dados no banco")

    return {"message": "Meta atualizada com sucesso"}




def get_arpu(db: Session):
    mrr = get_mrr(db)
    active = get_active_subscriptions(db)
    return mrr / active if active > 0 else 0.0


# =========================================================
# CHURN
# =========================================================

def get_churn_rate(db: Session):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    total_start = db.query(Subscription).filter(
        Subscription.created_at < thirty_days_ago
    ).count()

    churned = db.query(Subscription).filter(
        Subscription.canceled_at != None,
        Subscription.canceled_at >= thirty_days_ago
    ).count()

    if total_start == 0:
        return 0.0

    return (churned / total_start) * 100


# =========================================================
# MRR HISTORY (GRÁFICO)
# =========================================================

def get_mrr_history(db: Session):
    history = []
    today = datetime.utcnow()

    for i in range(5, -1, -1):
        date = today - timedelta(days=i * 30)
        month_name = date.strftime("%b")

        mrr_value = db.query(func.sum(Plan.price))\
            .select_from(Subscription)\
            .join(Plan, Subscription.plan_id == Plan.id)\
            .filter(Subscription.is_active == True)\
            .scalar() or 0

        history.append({
            "month": month_name,
            "mrr": float(mrr_value)
        })

    return history


# =========================================================
# CLIENTES EM RISCO
# =========================================================

def get_at_risk_clients(db: Session):
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    clients = db.query(Client).filter(
        Client.last_activity_at != None,
        Client.last_activity_at < seven_days_ago
    ).order_by(Client.last_activity_at.asc()).limit(5).all()

    at_risk = []

    for client in clients:
        delta = now - client.last_activity_at.replace(tzinfo=None)

        at_risk.append({
            "id": client.id,
            "name": client.name,
            "last_login_days": delta.days,
            "status": "inactive"
        })

    return at_risk


# =========================================================
# ACTIVITY LOG (THE PULSE)
# =========================================================

def get_recent_activity(db: Session):
    activities = []
    now_utc = datetime.now(timezone.utc)

    # 1. BUSCAR USUÁRIOS
    users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    for u in users:
        # Se não tiver data no banco, usa 'now' para não sumir da lista
        dt = u.created_at if u.created_at else now_utc
        activities.append({
            "id": f"user_{u.id}",
            "message": f"Novo usuário: {u.email}",
            "type": "user",
            "created_at": dt
        })

    # 2. BUSCAR ASSINATURAS (Aqui estão seus 3 registros!)
    subs = db.query(Subscription).order_by(Subscription.created_at.desc()).limit(5).all()
    for s in subs:
        dt = s.created_at if s.created_at else now_utc
        activities.append({
            "id": f"sub_{s.id}",
            "message": "Nova assinatura confirmada",
            "type": "money",
            "created_at": dt
        })

    # 3. ORDENAÇÃO SEGURA (Garante que os mais novos fiquem no topo)
    activities.sort(
        key=lambda x: x["created_at"].replace(tzinfo=timezone.utc) if x["created_at"].tzinfo is None else x["created_at"],
        reverse=True
    )

    # 4. CONVERSÃO PARA STRING (O que o Frontend entende)
    for act in activities:
        dt = act["created_at"]
        if isinstance(dt, datetime):
            # Garante que o 'Z' (UTC) vá na string para o JS entender a hora
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            act["created_at"] = dt.isoformat()

    return activities[:10]




# =========================================================
# ACTIVITY DETALHADA (CADASTROS + SESSÕES)
# =========================================================

from datetime import datetime, timedelta, timezone

def get_detailed_activity(db: Session):
    def get_user_display(u):
        return getattr(u, "name", None) or u.email

    # Usamos o timezone.utc para garantir que a comparação no banco e a 
    # serialização sigam o mesmo padrão que o frontend espera
    now = datetime.now(timezone.utc)

    # --- NOVOS CADASTROS ---
    new_accounts = db.query(User)\
        .filter(User.created_at != None)\
        .order_by(User.created_at.desc())\
        .limit(5)\
        .all()

    accounts_log = []
    for u in new_accounts:
        # Forçamos a data a ser tratada como UTC antes de converter para texto
        dt_utc = u.created_at.replace(tzinfo=timezone.utc) if u.created_at.tzinfo is None else u.created_at
        
        accounts_log.append({
            "id": f"new_{u.id}",
            "user": get_user_display(u),
            "time": dt_utc.isoformat()
        })

    # --- SESSÕES ATIVAS (Últimos 5 minutos) ---
    five_minutes_ago = now - timedelta(minutes=15)

    sessions = db.query(User)\
        .filter(
            User.last_login != None,
            User.last_login >= five_minutes_ago
        )\
        .order_by(User.last_login.desc())\
        .limit(5)\
        .all()

    sessions_log = []
    for u in sessions:
        dt_utc = u.last_login.replace(tzinfo=timezone.utc) if u.last_login.tzinfo is None else u.last_login
        
        sessions_log.append({
            "id": f"sess_{u.id}",
            "user": get_user_display(u),
            "time": dt_utc.isoformat(),
            "action": "ativo agora"
        })

    return {
        "accounts": accounts_log,
        "sessions": sessions_log
    }

