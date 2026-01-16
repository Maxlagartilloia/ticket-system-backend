from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# =========================
# AUTH
# =========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


# =========================
# USERS
# =========================
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


# =========================
# INSTITUTIONS
# =========================
class InstitutionBase(BaseModel):
    name: str
    address: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionOut(InstitutionBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# DEPARTMENTS
# =========================
class DepartmentBase(BaseModel):
    name: str
    institution_id: int


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# TICKETS
# =========================
class TicketBase(BaseModel):
    title: str
    description: str
    priority: str
    institution_id: int
    equipment_id: Optional[int] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None


class TicketOut(TicketBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# DASHBOARD
# =========================
class DashboardStats(BaseModel):
    open_tickets: int
    in_progress: int
    resolved_today: int
    institutions: int
