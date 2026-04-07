from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.insight import Insight
from app.models.client import Tenant
from app.schemas.insight_schema import InsightCreate, InsightResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/insights", tags=["Insights"])


# 🔹 CREATE INSIGHT
@router.post("/", response_model=InsightResponse)
def create_insight(
    insight_data: InsightCreate,
    client_id: str = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    client = (
        db.query(Tenant)
        .filter(
            Tenant.id == client_id,
            Tenant.owner_id == current_user.id
        )
        .first()
    )

    if not client:
        raise HTTPException(status_code=403, detail="Invalid client")

    new_insight = Insight(
        content=insight_data.content,
        category=insight_data.category,
        user_id=current_user.id,
        client_id=client_id
    )

    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)

    return new_insight


# LIST INSIGHTS (com paginação + filtros + segurança)
@router.get("/", response_model=list[InsightResponse])
def list_insights(
    client_id: str = Query(...),
    limit: int = Query(10, le=100),
    offset: int = Query(0, ge=0),
    category: str | None = Query(None, max_length=50),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    client = (
        db.query(Tenant)
        .filter(
            Tenant.id == client_id,
            Tenant.owner_id == current_user.id
        )
        .first()
    )

    if not client:
        raise HTTPException(status_code=403, detail="Invalid client")

    query = db.query(Insight).filter(
        Insight.tenant_id == client_id
    )

    # filtro opcional por categoria
    if category:
        query = query.filter(Insight.category == category)

    insights = (
        query
        .order_by(Insight.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return insights


# 🔹 UPDATE INSIGHT
@router.put("/{insight_id}", response_model=InsightResponse)
def update_insight(
    insight_id: int,
    insight_data: InsightCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    insight = (
        db.query(Insight)
        .join(Client)
        .filter(
            Insight.id == insight_id,
            Client.owner_id == current_user.id
        )
        .first()
    )

    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")

    insight.content = insight_data.content
    insight.category = insight_data.category

    db.commit()
    db.refresh(insight)

    return insight


# 🔹 DELETE INSIGHT
@router.delete("/{insight_id}")
def delete_insight(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    insight = (
        db.query(Insight)
        .join(Client)
        .filter(
            Insight.id == insight_id,
            Client.owner_id == current_user.id
        )
        .first()
    )

    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")

    db.delete(insight)
    db.commit()

    return {"message": "Insight deleted"}