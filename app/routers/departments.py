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

@router.post("/", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: schemas.DepartmentCreate, 
    db: Session = Depends(get_db),
    _ = Depends(require_supervisor)
):
    # Validar que la institución exista
    inst = db.query(models.Institution).filter(models.Institution.id == payload.institution_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    new_dept = models.Department(**payload.dict())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/institution/{institution_id}", response_model=List[schemas.DepartmentOut])
def list_departments_by_institution(institution_id: int, db: Session = Depends(get_db)):
    return db.query(models.Department).filter(models.Department.institution_id == institution_id).all()
