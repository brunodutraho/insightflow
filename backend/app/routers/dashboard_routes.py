from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database.database import get_db
from app.auth.dependencies import get_current_user, validate_hierarchy_access
from app.models.user import User, UserRole

from app.services.kpi_service import get_kpis_data
from app.services.score_service import calculate_score
from app.services.insight_service import generate_insights
from app.services.social_service import get_latest_social_metrics
from app.services.plan_service import has_feature
from app.auth.dependencies import require_access

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard(
    client_id: int = Query(...),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_access([
        UserRole.admin_master,
        UserRole.gerente,
        UserRole.gestor_interno,
        UserRole.gestor_assinante,
        UserRole.cliente_final
    ]))
):
    
    target_client_id = client_id
    
    user_role = user.role.value if hasattr(user.role, "value") else user.role
    
    if user_role == UserRole.cliente_final or user_role == "cliente_final":
        if user.tenant_id != client_id:
            target_client_id = user.tenant_id
    
    validate_hierarchy_access(target_client_id, user, db)

    kpis = get_kpis_data(db, target_client_id, start_date, end_date)
    summary = kpis.get("summary", {})
    timeseries = kpis.get("timeseries", [])

    insights = generate_insights(summary)

    social_data = get_latest_social_metrics(db, target_client_id)

    score_enabled = has_feature(db, user.tenant_id, "score") or user_role == "admin"

    score_data = None
    overview = None

    if score_enabled:
        score_result = calculate_score(summary)
        
        score_data = {
            "value": score_result.get("score"),
            "level": score_result.get("level"),
            "details": score_result.get("details"),
        }

        overview = {
            "score": score_result.get("score"),
            "level": score_result.get("level"),
            "status": _get_status_label(score_result.get("level"))
        }
    else:
        # Visão de Up-sell para quem não tem o plano
        score_data = {
            "available": False,
            "message": "Faça upgrade para o plano Pro para ver seu Score de Performance."
        }
        overview = {
            "score": None,
            "level": None,
            "status": "bloqueado"
        }

    return {
        "overview": overview,
        "kpis": {
            "summary": summary,
            "timeseries": timeseries
        },
        "insights": insights,
        "social": social_data,
        "score": score_data,
        "features": {
            "score_enabled": score_enabled
        },
        "client_context_id": target_client_id # Para o front saber qual ID está sendo exibido
    }

def _get_status_label(level: str | None):
    if not level:
        return "desconhecido"

    mapping = {
        "excellent": "excelente",
        "good": "em melhoria",
        "average": "estável",
        "poor": "crítico"
    }

    return mapping.get(level, "desconhecido")
