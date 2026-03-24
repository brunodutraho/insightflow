from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["Users"])

# Qualquer usuário autenticado
@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return {
        "id": user["user_id"], 
        "role": user["role"] 
    }

# Apenas Admin
@router.get("/admin")
def admin_route(user: dict = Depends(require_roles(["admin"]))):
    return {
        "message": "Admin access granted",
        "user": {
            "id": user["user_id"],
            "role": user["role"]
        }
    }

# Admin + Gestor
@router.get("/dashboard")
def dashboard(user: dict = Depends(require_roles(["admin", "gestor"]))):
    return {
        "message": "Dashboard access granted",
        "user": {
            "id": user["user_id"],
            "role": user["role"]
        }
    }
