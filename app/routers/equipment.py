from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter()


# =========================
# CREATE EQUIPMENT
# =========================
@router.post(
    "/",
    response_model=schemas.EquipmentOut,
    status_code=status.HTTP_201_CREATED
)
def create_equipment(
    equipment: schemas.EquipmentCreate,
    db: Session = Depends(get_db)
):
    new_equipment = models.Equipment(**equipment.dict())
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
    return (
        db.query(models.Equipment)
        .filter(models.Equipment.department_id == department_id)
        .order_by(models.Equipment.name)
        .all()
    )
