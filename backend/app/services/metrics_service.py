from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta, timezone

import calendar
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
from app.models.client import Tenant  # Renamed from Client
from app.models.app_config import AppConfig
from app.auth.utils import verify_password
from app.models.activity import ActivityItem 
from app.models.goal import GoalHistory


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
    return db.query(Tenant).count()


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


# ================================
# GET - META + PACING (RITMO)
# ================================

def get_mrr_pacing(db: Session):
    """ Fonte Única de Verdade: GoalHistory """
    now = datetime.now()

    # Busca a meta mais recente criada para este mês/ano
    goal_record = db.query(GoalHistory).filter(
        extract('month', GoalHistory.month_reference) == now.month,
        extract('year', GoalHistory.month_reference) == now.year
    ).order_by(GoalHistory.created_at.desc()).first()

    target = goal_record.target_value if goal_record else 10000.0
    
    _, total_days = calendar.monthrange(now.year, now.month)
    expected_progress = (now.day / total_days) * 100

    return {
        "target": float(target),
        "expected_progress": round(expected_progress, 1)
    }

def update_mrr_goal(db: Session, user: User, new_goal: float, password: str):
    # 1. Valida Senha (Segurança)
    if not verify_password(password, user.hashed_password):
        raise Exception("Senha inválida")

    # 2. Cria o novo registro no Histórico (Versionamento)
    now = datetime.now()
    new_record = GoalHistory(
        target_value=new_goal,
        month_reference=now.replace(day=1), # Referência ao início do mês
        created_at=now
    )
    db.add(new_record)
    
    # 3. Log de Atividade para a Timeline
    log = ActivityItem(
        type="configuracao",
        message=f"Meta de MRR atualizada para R$ {new_goal:,.2f}",
        created_at=now
    )
    db.add(log)

    db.commit()
    return {"message": "Meta atualizada no histórico", "target": new_goal}





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
    today = datetime.now()

    # Buscamos os últimos 6 meses para o gráfico
    for i in range(5, -1, -1):
        # Calcula o primeiro dia do mês alvo no loop
        # Subtraímos meses de forma segura
        target_date = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        month_label = target_date.strftime("%b")

        # 1. Busca o MRR Real (Baseado no que você já tinha)
        mrr_real = db.query(func.sum(Plan.price))\
            .select_from(Subscription)\
            .join(Plan, Subscription.plan_id == Plan.id)\
            .filter(Subscription.is_active == True)\
            .scalar() or 0

        # 2. Busca a meta registrada para este MÊS e ANO específicos
        goal_record = db.query(GoalHistory)\
            .filter(
                extract('month', GoalHistory.month_reference) == target_date.month,
                extract('year', GoalHistory.month_reference) == target_date.year
            )\
            .order_by(GoalHistory.created_at.desc())\
            .first()
            
        # Fallback: Se não houver meta gravada para o mês passado, usa 10k
        target_goal = goal_record.target_value if goal_record else 10000.0

        history.append({
            "month": month_label,
            "mrr": float(mrr_real),
            "goal": target_goal # Cada ponto do gráfico agora tem sua própria meta "congelada"
        })

    return history

def update_mrr_goal(db: Session, user, new_goal: float, password: str):
    # ... (sua lógica de validação de senha aqui) ...

    now = datetime.now()
    month_ref = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Cria um novo registro de histórico em vez de apenas dar update
    # Isso é o que garante a "memória" do gráfico
    new_history = GoalHistory(
        target_value=new_goal,
        month_reference=month_ref,
        updated_by=user.email
    )
    
    db.add(new_history)
    db.commit()
    
    # ... (lógica de salvar atividade na timeline) ...
    return {"message": "Meta atualizada e registrada no histórico"}



# =========================================================
# CLIENTES EM RISCO
# =========================================================

def get_at_risk_clients(db: Session):
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    clients = db.query(Tenant).filter(
        Tenant.last_activity_at != None,
        Tenant.last_activity_at < seven_days_ago
    ).order_by(Tenant.last_activity_at.asc()).limit(5).all()

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

    # Helper para formatar itens
    def format_activity(id_prefix, obj, message, type_name, priority, date_field):
        val = getattr(obj, date_field)
        return {
            "id": f"{id_prefix}_{obj.id}",
            "message": message,
            "type": type_name,
            "priority": priority,
            "created_at": val.replace(tzinfo=timezone.utc).isoformat() if val else None
        }

    # Queries otimizadas com limit
    new_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    new_subs = db.query(Subscription).filter(Subscription.canceled_at == None).order_by(Subscription.created_at.desc()).limit(5).all()
    churn = db.query(Subscription).filter(Subscription.canceled_at != None).order_by(Subscription.canceled_at.desc()).limit(5).all()

    for u in new_users:
        activities.append(format_activity("user", u, f"Novo cadastro: {u.email}", "user", "low", "created_at"))
        
    for s in new_subs:
        activities.append(format_activity("sub", s, "Nova assinatura Pro", "money", "medium", "created_at"))

    for c in churn:
        activities.append(format_activity("churn", c, "Assinatura cancelada", "alert", "high", "canceled_at"))

    # Ordenação única e slice final
    activities.sort(key=lambda x: x["created_at"] or "", reverse=True)
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

def get_trial_to_paid_funnel(db: Session):
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)

    # usuários criados (trial)
    trials = db.query(User).filter(
        User.created_at >= thirty_days_ago
    ).count()

    # assinaturas criadas
    conversions = db.query(Subscription).filter(
        Subscription.created_at >= thirty_days_ago
    ).count()

    # taxa
    rate = (conversions / trials) * 100 if trials > 0 else 0

    return {
        "trials": trials,
        "conversions": conversions,
        "conversion_rate": rate
    }

    
def get_smart_insights(db: Session):
    insights = []

    # métricas base
    mrr = get_mrr(db)
    churn = get_churn_rate(db)
    growth = get_users_growth_rate(db)
    conversion_data = get_trial_to_paid_funnel(db)
    conversion = conversion_data["conversion_rate"]

    # =========================
    # REGRAS INTELIGENTES
    # =========================

    # 🚨 churn alto
    if churn > 5:
        insights.append({
            "type": "danger",
            "message": "Churn alto detectado — clientes estão cancelando rápido"
        })

    # ⚠️ conversão baixa
    if conversion < 5:
        insights.append({
            "type": "warning",
            "message": "Baixa conversão de trial → pago — revise onboarding ou oferta"
        })

    # ⚠️ crescimento sem receita
    if growth > 10 and mrr == 0:
        insights.append({
            "type": "warning",
            "message": "Usuários estão crescendo mas não geram receita"
        })

    # 🟢 saudável
    if churn < 3 and conversion > 10:
        insights.append({
            "type": "success",
            "message": "Produto saudável: boa retenção e conversão"
        })

    # fallback
    if not insights:
        insights.append({
            "type": "info",
            "message": "Dados insuficientes para análise avançada"
        })

    return insights

def log_admin_action(db, admin_id, target_id, action):
    from app.models.admin_log import AdminLog
    log = AdminLog(admin_id=admin_id, target_user_id=target_id, action=action)
    db.add(log)
    # O commit é feito na rota
