from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Usuario, Institucion
from app.dependencies import require_roles
from app.auth import hash_password

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# =========================
# CREAR USUARIO
# =========================
@router.post("/", dependencies=[Depends(require_roles("admin", "supervisor"))])
def crear_usuario(
    nombre: str,
    email: str,
    password: str,
    rol: str,
    institucion_id: int = None,
    db: Session = Depends(get_db)
):
    if rol not in ["admin", "supervisor", "tecnico", "cliente"]:
        raise HTTPException(status_code=400, detail="Rol no válido")

    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    if rol == "cliente":
        if not institucion_id:
            raise HTTPException(status_code=400, detail="Cliente requiere institucion_id")

        institucion = db.query(Institucion).filter(Institucion.id == institucion_id).first()
        if not institucion:
            raise HTTPException(status_code=404, detail="Institución no existe")

    usuario = Usuario(
        nombre=nombre,
        email=email,
        password=hash_password(password),
        rol=rol,
        institucion_id=institucion_id
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# =========================
# LISTAR USUARIOS
# =========================
@router.get("/", dependencies=[Depends(require_roles("admin", "supervisor"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).order_by(Usuario.id).all()


# =========================
# OBTENER USUARIO
# =========================
@router.get("/{usuario_id}", dependencies=[Depends(require_roles("admin", "supervisor"))])
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
