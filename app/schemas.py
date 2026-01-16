from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# =========================
# AUTH SCHEMAS
# =========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str

# =========================
# USERS SCHEMAS
# =========================
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str  # 'admin', 'supervisor', 'technician', 'client'
    institution_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# =========================
# INSTITUTIONS SCHEMAS
# =========================
class InstitutionBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionOut(InstitutionBase):
    id: int

    class Config:
        from_attributes = True

# =========================
# DEPARTMENTS SCHEMAS
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
# EQUIPMENT SCHEMAS
# =========================
class EquipmentBase(BaseModel):
    name: str
    model: Optional[str] = None
    serial_number: Optional[str] = None
    department_id: int

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentOut(EquipmentBase):
    id: int

    class Config:
        from_attributes = True

# =========================
# TICKETS SCHEMAS
# =========================
class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    institution_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketOut(TicketBase):
    id: int
    status: str
    created_at: datetime
    creator_id: int

    class Config:
        from_attributes = True

# =========================
# DASHBOARD SCHEMAS
# =========================
class DashboardStats(BaseModel):
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    total_institutions: int
