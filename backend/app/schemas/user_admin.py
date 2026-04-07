from pydantic import BaseModel, EmailStr
from typing import Optional, List


# Resposta básica do usuário (tabela)
class UserAdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    last_login_days: Optional[int]
    health_status: str

    class Config:
        from_attributes = True


# Filtros via query params
class UserFilters(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    search: Optional[str] = None


# Atualizar email
class UpdateEmailRequest(BaseModel):
    new_email: EmailStr


# Reset de senha (admin)
class ResetPasswordRequest(BaseModel):
    new_password: str


# Dar dias grátis
class GrantDaysRequest(BaseModel):
    days: int


# Criar usuário interno (staff)
class CreateStaffRequest(BaseModel):
    name: str
    email: EmailStr
    password: str