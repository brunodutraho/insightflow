from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["Users"])


# Any authenticated user
@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return user


# Admin only
@router.get("/admin")
def admin_route(user = Depends(require_roles(["admin"]))):
    return {"message": "Admin access"}


# Admin + Manager
@router.get("/dashboard")
def dashboard(user = Depends(require_roles(["admin", "gestor"]))):
    return {"message": "Dashboard access"}