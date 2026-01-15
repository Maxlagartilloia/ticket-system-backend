from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ---------- AUTH ----------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    rol: str


# ---------- USUARIOS ----------

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str
    institucion_id: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


# ---------- INSTITUCIONES ----------

class InstitucionBase(BaseModel):
    nombre: str
    contrato: str


class InstitucionOut(InstitucionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- TICKETS ----------

class TicketBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None


class TicketCreate(TicketBase):
    institucion_id: int


class TicketOut(TicketBase):
    id: int
    estado: str
    institucion_id: int
    tecnico_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
