from pydantic import BaseModel
from typing import Optional

# -------- USUARIOS --------
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    rol: str

class UsuarioOut(UsuarioCreate):
    id: int
    class Config:
        orm_mode = True


# -------- INSTITUCIONES --------
class InstitucionCreate(BaseModel):
    nombre: str

class InstitucionOut(InstitucionCreate):
    id: int
    class Config:
        orm_mode = True


# -------- TICKETS --------
class TicketCreate(BaseModel):
    descripcion: str
    prioridad: str
    institucion_id: int

class TicketUpdate(BaseModel):
    estado: Optional[str] = None
    tecnico_id: Optional[int] = None

class TicketOut(BaseModel):
    id: int
    descripcion: str
    prioridad: str
    estado: str
    institucion_id: int
    tecnico_id: Optional[int]

    class Config:
        orm_mode = True
