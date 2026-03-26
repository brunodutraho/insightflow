from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database.database import get_db
from app.auth.dependencies import get_current_user, validate_client_access

from app.services.kpi_service import get_kpis_data
from app.services.score_service import calculate_score
from app.services.insight_service import generate_insights
from app.services.social_service import get_latest_social_metrics
from app.services.feature_service import check_feature_access

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard(
    client_id: int = Query(...),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Segurança (multi-tenant)
    validate_client_access(client_id, user, db)

    # KPIs
    kpis = get_kpis_data(db, client_id, start_date, end_date)

    summary = kpis.get("summary", {})
    timeseries = kpis.get("timeseries", [])

    # Insights estruturados
    insights = generate_insights(summary)

    # Social
    social_data = get_latest_social_metrics(db, client_id)

    # Feature: Score
    score_enabled = check_feature_access(user.id, db, "score")

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
        score_data = {
            "available": False,
            "message": "Upgrade your plan to access performance score"
        }

        overview = {
            "score": None,
            "level": None,
            "status": "locked"
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
        }
    }


def _get_status_label(level: str | None):
    if not level:
        return "unknown"

    mapping = {
        "excellent": "excellent",
        "good": "improving",
        "average": "stable",
        "poor": "critical"
    }

    return mapping.get(level, "unknown")