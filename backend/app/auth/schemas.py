from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


# 🔐 LOGIN
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 🚀 REGISTER (ONBOARDING COMPLETO)
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    phone: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    company_name: Optional[str] = None
    team_size: Optional[int] = None
    how_heard: Optional[str] = None
    terms_accepted: bool = False


# 👤 RESPONSE
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    tenant_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    full_name: Optional[str] = None
    status: str
    email_verified: bool

    class Config:
        from_attributes = True


class ClientUserCreate(BaseModel):
    email: EmailStr
    tenant_id: UUID

class RegisterResponse(BaseModel):
    user: UserResponse
    message: str