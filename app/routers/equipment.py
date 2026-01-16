from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import require_supervisor

router = APIRouter(
    tags=["Equipment"]
)

# =========================
# CREATE EQUIPMENT
# =========================
@router.post(
    "/",
    response_model=schemas.EquipmentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_supervisor)]
)
def create_equipment(
    equipment: schemas.EquipmentCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el departamento exista
    department = (
        db.query(models.Department)
        .filter(models.Department.id == equipment.department_id)
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    # Verificar que la institución del departamento esté activa
    institution = (
        db.query(models.Institution)
        .filter(
            models.Institution.id == department.institution_id,
            models.Institution.is_active == True
        )
        .first()
    )

    if not institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution is inactive"
        )

    new_equipment = models.Equipment(
        name=equipment.name,
        model=equipment.model,
        serial_number=equipment.serial_number,
        department_id=equipment.department_id
    )

    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)

    return new_equipment


# =========================
# LIST EQUIPMENT (BY DEPARTMENT)
# =========================
@router.get(
    "/department/{department_id}",
    response_model=List[schemas.EquipmentOut]
)
def list_equipment_by_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    # Verificar que el departamento exista
    department = (
        db.query(models.Department)
        .filter(models.Department.id == department_id)
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    # Verificar que la institución esté activa
    institution = (
        db.query(models.Institution)
        .filter(
            models.Institution.id == department.institution_id,
            models.Institution.is_active == True
        )
        .first()
    )

    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found or inactive"
        )

    return (
        db.query(models.Equipment)
        .filter(models.Equipment.department_id == department_id)
        .order_by(models.Equipment.name.asc())
        .all()
    )
