from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.database.database import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


# 🔐 USER LOGADO
@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return {
        "id": user["user_id"],
        "role": user["role"]
    }


# 🔐 ADMIN
@router.get("/admin")
def admin_route(user: dict = Depends(require_roles(["admin"]))):
    return {
        "message": "Admin access granted",
        "user": user
    }


# 🔐 DASHBOARD
@router.get("/dashboard")
def dashboard(user: dict = Depends(require_roles(["admin", "gestor"]))):
    return {
        "message": "Dashboard access granted",
        "user": user
    }


# 🔥 LISTAR USUÁRIOS (ADMIN)
@router.get("/")
def list_users(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["admin"]))
):
    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at
        }
        for u in users
    ]


# 🔥 ALTERAR ROLE
@router.patch("/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str = Body(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["admin"]))
):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user.role = role
    db.commit()

    return {"message": "Role updated"}


# 🔥 DELETAR USUÁRIO
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["admin"]))
):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(target_user)
    db.commit()

    return {"message": "User deleted"}