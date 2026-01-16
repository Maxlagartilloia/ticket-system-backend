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

# Se define como UserOut para que el router de usuarios lo encuentre
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

# Se define como InstitutionOut porque el router de instituciones lo pide así
class InstitutionOut(InstitutionBase):
    id: int
    class Config:
        from_attributes = True

class Institution(InstitutionOut):
    pass

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

# Se define como TicketOut para que el router de tickets funcione
class TicketOut(TicketBase):
    id: int
    created_at: datetime
    creator_id: int
    assigned_to: Optional[int] = None
    class Config:
        from_attributes = True

# --- ESTADÍSTICAS DEL DASHBOARD ---
class DashboardStats(BaseModel):
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    total_institutions: int
