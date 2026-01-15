from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Institucion
from app.dependencies import require_roles

router = APIRouter(prefix="/instituciones", tags=["Instituciones"])


@router.post("/", dependencies=[Depends(require_roles("admin", "supervisor"))])
def crear_institucion(nombre: str, contrato: str, db: Session = Depends(get_db)):
    inst = Institucion(nombre=nombre, contrato=contrato)
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst


@router.get("/", dependencies=[Depends(require_roles("admin", "supervisor"))])
def listar_instituciones(db: Session = Depends(get_db)):
    return db.query(Institucion).all()
