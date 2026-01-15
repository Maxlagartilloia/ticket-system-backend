from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# =========================
# AUTH / USERS
# =========================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # admin | supervisor | technician | client


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

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
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# TICKETS
# =========================

class TicketBase(BaseModel):
    institution_id: int
    equipment: str
    description: str
    priority: str  # low | medium | high


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    technician_id: Optional[int] = None
    status: Optional[str] = None  # open | in_progress | closed
    priority: Optional[str] = None


class TicketOut(TicketBase):
    id: int
    status: str
    created_at: datetime
    technician_id: Optional[int] = None

    class Config:
        from_attributes = True


# =========================
# REPORTS (BASIC)
# =========================

class DashboardStats(BaseModel):
    open_tickets: int
    in_progress: int
    resolved_today: int
    institutions: int
