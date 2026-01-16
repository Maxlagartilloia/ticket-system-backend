from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import require_supervisor

router = APIRouter(
    prefix="/institutions",
    tags=["Institutions"]
)

# =========================
# CREATE INSTITUTION
# =========================
@router.post(
    "/",
    response_model=schemas.InstitutionOut,
    status_code=status.HTTP_201_CREATED
)
def create_institution(
    institution: schemas.InstitutionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_supervisor)
):
    existing = (
        db.query(models.Institution)
        .filter(models.Institution.name == institution.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution already exists"
        )

    new_institution = models.Institution(
        name=institution.name,
        address=institution.address
    )

    db.add(new_institution)
    db.commit()
    db.refresh(new_institution)

    return new_institution


# =========================
# LIST INSTITUTIONS
# =========================
@router.get(
    "/",
    response_model=List[schemas.InstitutionOut]
)
def list_institutions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_supervisor)
):
    return (
        db.query(models.Institution)
        .order_by(models.Institution.name.asc())
        .all()
    )


# =========================
# GET INSTITUTION BY ID
# =========================
@router.get(
    "/{institution_id}",
    response_model=schemas.InstitutionOut
)
def get_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_supervisor)
):
    institution = (
        db.query(models.Institution)
        .filter(models.Institution.id == institution_id)
        .first()
    )

    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )

    return institution


# =========================
# UPDATE INSTITUTION
# =========================
@router.put(
    "/{institution_id}",
    response_model=schemas.InstitutionOut
)
def update_institution(
    institution_id: int,
    institution: schemas.InstitutionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_supervisor)
):
    db_institution = (
        db.query(models.Institution)
        .filter(models.Institution.id == institution_id)
        .first()
    )

    if not db_institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )

    db_institution.name = institution.name
    db_institution.address = institution.address

    db.commit()
    db.refresh(db_institution)

    return db_institution


# =========================
# DELETE INSTITUTION
# =========================
@router.delete(
    "/{institution_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_supervisor)
):
    institution = (
        db.query(models.Institution)
        .filter(models.Institution.id == institution_id)
        .first()
    )

    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )

    db.delete(institution)
    db.commit()
