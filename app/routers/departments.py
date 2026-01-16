from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import require_supervisor

router = APIRouter(
    tags=["Departments"]
)

# =========================
# CREATE DEPARTMENT
# =========================
@router.post(
    "/",
    response_model=schemas.DepartmentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_supervisor)]
)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
):
    # Verificar que la institución exista y esté activa
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

    new_department = models.Department(
        name=department.name,
        institution_id=department.institution_id
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


# =========================
# LIST DEPARTMENTS (ONLY ACTIVE INSTITUTIONS)
# =========================
@router.get(
    "/",
    response_model=List[schemas.DepartmentOut]
)
def list_departments(
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Department)
        .join(models.Institution)
        .filter(models.Institution.is_active == True)
        .order_by(models.Department.name.asc())
        .all()
    )


# =========================
# LIST BY INSTITUTION
# =========================
@router.get(
    "/institution/{institution_id}",
    response_model=List[schemas.DepartmentOut]
)
def list_departments_by_institution(
    institution_id: int,
    db: Session = Depends(get_db)
):
    # Verificar institución activa
    institution = (
        db.query(models.Institution)
        .filter(
            models.Institution.id == institution_id,
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
        db.query(models.Department)
        .filter(models.Department.institution_id == institution_id)
        .order_by(models.Department.name.asc())
        .all()
    )


# =========================
# DELETE DEPARTMENT (SAFE DELETE)
# =========================
@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_supervisor)]
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
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

    # Evitar borrar si tiene equipment asociado
    equipment_exists = (
        db.query(models.Equipment)
        .filter(models.Equipment.department_id == department.id)
        .first()
    )

    if equipment_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department with associated equipment"
        )

    db.delete(department)
    db.commit()

