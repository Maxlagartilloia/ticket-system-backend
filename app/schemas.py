from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- USUARIOS ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    is_active: Optional[bool] = True
    institution_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

# 🚨 Se llama UserOut porque así lo pide el router de usuarios
class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- INSTITUCIONES ---
class InstitutionBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class InstitutionCreate(InstitutionBase):
    pass

class Institution(InstitutionBase):
    id: int
    class Config:
        from_attributes = True

# --- TICKETS ---
class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"
    institution_id: int
    equipment_id: Optional[int] = None

class TicketCreate(TicketBase):
    pass

# 🚨 Se llama TicketOut porque así lo pide el router de tickets
class TicketOut(TicketBase):
    id: int
    created_at: datetime
    creator_id: int
    assigned_to: Optional[int] = None
    class Config:
        from_attributes = True

# --- ESTADÍSTICAS ---
class DashboardStats(BaseModel):
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    total_institutions: int
