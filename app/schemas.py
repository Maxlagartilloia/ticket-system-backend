from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# =========================
# USERS
# =========================

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str  # admin | supervisor | technician | client


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# =========================
# INSTITUTIONS
# =========================

class InstitutionBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionOut(InstitutionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


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
        orm_mode = True


# =========================
# EQUIPMENT
# =========================

class EquipmentBase(BaseModel):
    brand: str
    model: str
    serial_number: Optional[str] = None
    department_id: int


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentOut(EquipmentBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# TICKETS
# =========================

class TicketBase(BaseModel):
    title: str
    description: str
    priority: str  # low | medium | high
    institution_id: int
    equipment_id: int


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    status: Optional[str] = None           # open | in_progress | closed
    technician_id: Optional[int] = None


class TicketOut(TicketBase):
    id: int
    status: str
    technician_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


# =========================
# AUTH
# =========================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

