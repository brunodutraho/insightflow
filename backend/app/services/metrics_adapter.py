from sqlalchemy.orm import Session
from app.models.metric import Metric

def get_metrics(db: Session, tenant_id: str, source: str):
    
    if source == "ads":
        return get_ads_metrics(db, tenant_id)

    elif source == "social":
        return get_social_metrics(db, tenant_id)

    elif source == "unified":
        return get_unified_metrics(db, tenant_id)

    else:
        return []