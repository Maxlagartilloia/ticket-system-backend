from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import require_supervisor

router = APIRouter(
    prefix="/departments",
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
    institution = (
        db.query(models.Institution)
        .filter(models.Institution.id == department.institution_id)
        .first()
    )

    if not institution:
        raise HTTPException(
            status_code=404,
            detail="Institution not found"
        )

    new_department = models.Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


# =========================
# LIST DEPARTMENTS
# =========================
@router.get(
    "/",
    response_model=List[schemas.DepartmentOut]
)
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).order_by(models.Department.name).all()


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
    return (
        db.query(models.Department)
        .filter(models.Department.institution_id == institution_id)
        .order_by(models.Department.name)
        .all()
    )


# =========================
# DELETE DEPARTMENT
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
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()
