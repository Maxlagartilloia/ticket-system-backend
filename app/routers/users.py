from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import require_admin, require_supervisor

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# =========================
# CREATE USER
# =========================
@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_supervisor)]
)
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Validar rol permitido
    if payload.role not in ["admin", "supervisor", "technician", "client"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )

    # Verificar email único
    existing = (
        db.query(models.User)
        .filter(models.User.email == payload.email)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Crear usuario
    user = models.User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=payload.password,  # hash se aplica en auth/bootstrap o flujo controlado
        role=payload.role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =========================
# LIST USERS
# =========================
@router.get(
    "/",
    response_model=List[schemas.UserOut],
    dependencies=[Depends(require_supervisor)]
)
def list_users(
    db: Session = Depends(get_db)
):
    return (
        db.query(models.User)
        .order_by(models.User.id.asc())
        .all()
    )


# =========================
# GET USER BY ID
# =========================
@router.get(
    "/{user_id}",
    response_model=schemas.UserOut,
    dependencies=[Depends(require_supervisor)]
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
