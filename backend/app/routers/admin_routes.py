from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.user import User, UserRole
from app.models.client import Client
from app.auth.dependencies import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_roles(["admin"]))]
)


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()

    role_counts = db.query(
        User.role,
        func.count(User.id)
    ).group_by(User.role).all()

    total_companies = db.query(Client).count()

    recent_managers = db.query(User).filter(
        User.role == UserRole.gestor
    ).order_by(User.created_at.desc()).limit(5).all()

    return {
        "summary": {
            "total_users": total_users,
            "total_companies": total_companies
        },
        "distribution": [
            {
                "role": role.value if hasattr(role, "value") else role,
                "count": count
            }
            for role, count in role_counts
        ],
        "recent_activity": [
            {
                "id": u.id,
                "email": u.email,
                "created_at": u.created_at
            }
            for u in recent_managers
        ]
    }


@router.get("/clients")
def list_all_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()