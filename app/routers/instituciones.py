from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Institucion
from app.schemas import InstitucionBase, InstitucionOut
from app.dependencies import require_roles

router = APIRouter(
    prefix="/instituciones",
    tags=["Instituciones"]
)


@router.post(
    "/",
    response_model=InstitucionOut,
    dependencies=[Depends(require_roles("admin", "supervisor"))]
)
def crear_institucion(
    data: InstitucionBase,
    db: Session = Depends(get_db)
):
    institucion = Institucion(**data.dict())
    db.add(institucion)
    db.commit()
    db.refresh(institucion)
    return institucion


@router.get(
    "/",
    response_model=List[InstitucionOut],
    dependencies=[Depends(require_roles("admin", "supervisor"))]
)
def listar_instituciones(db: Session = Depends(get_db)):
    return db.query(Institucion).order_by(Institucion.id).all()


@router.get(
    "/{institucion_id}",
    response_model=InstitucionOut,
    dependencies=[Depends(require_roles("admin", "supervisor"))]
)
def obtener_institucion(
    institucion_id: int,
    db: Session = Depends(get_db)
):
    institucion = db.query(Institucion).filter(
        Institucion.id == institucion_id
    ).first()

    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")

    return institucion
