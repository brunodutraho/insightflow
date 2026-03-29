from pydantic import BaseModel, EmailStr
from typing import Optional


# 🔐 LOGIN
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 🚀 REGISTER (ONBOARDING COMPLETO)
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    phone: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    agency_name: Optional[str] = None
    company_size: Optional[str] = None
    source: Optional[str] = None


# 👤 RESPONSE
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    client_id: Optional[int] = None
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True


# 👥 GESTOR CRIANDO CLIENTE
class ClientUserCreate(BaseModel):
    email: EmailStr
    password: str
    client_id: int