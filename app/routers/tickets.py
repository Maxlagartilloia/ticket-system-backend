from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import (
    get_current_user,
    require_supervisor,
    require_technician,
    require_client
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

# =========================
# CREATE TICKET (CLIENT ONLY)
# =========================
@router.post(
    "/",
    response_model=schemas.TicketOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_client)]
)
def create_ticket(
    payload: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Validar institución existente y activa
    institution = (
        db.query(models.Institution)
        .filter(
            models.Institution.id == payload.institution_id,
            models.Institution.is_active == True
        )
        .first()
    )

    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found or inactive"
        )

    # 2. Validar equipo si se proporciona
    final_equipment_id = None
    if payload.equipment_id:
        equipment = (
            db.query(models.Equipment)
            .filter(models.Equipment.id == payload.equipment_id)
            .first()
        )

        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipment not found"
            )

        # 3. Validar pertenencia del equipo a la institución
        department = (
            db.query(models.Department)
            .filter(models.Department.id == equipment.department_id)
            .first()
        )

        if not department or department.institution_id != institution.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Equipment does not belong to this institution"
            )
        
        final_equipment_id = equipment.id

    # 4. Crear instancia según ADN
    new_ticket = models.Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status="open",
        institution_id=payload.institution_id,
        equipment_id=final_equipment_id,
        created_by=current_user.id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# =========================
# LIST TICKETS (ROLE-BASED VIEW)
# =========================
@router.get(
    "/",
    response_model=List[schemas.TicketOut]
)
def list_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Ticket)

    # Filtros de seguridad por rol
    if current_user.role in ["admin", "supervisor"]:
        return query.order_by(models.Ticket.created_at.desc()).all()

    if current_user.role == "technician":
        return query.filter(models.Ticket.assigned_to == current_user.id)\
                    .order_by(models.Ticket.created_at.desc()).all()

    # Clientes solo ven sus propios tickets
    return query.filter(models.Ticket.created_by == current_user.id)\
                .order_by(models.Ticket.created_at.desc()).all()


# =========================
# ASSIGN TECHNICIAN (SUPERVISOR ONLY)
# =========================
@router.put(
    "/{ticket_id}/assign",
    response_model=schemas.TicketOut,
    dependencies=[Depends(require_supervisor)]
)
def assign_technician(
    ticket_id: int,
    technician_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.status == "closed":
        raise HTTPException(status_code=400, detail="Cannot assign a closed ticket")

    # Validar técnico apto
    technician = db.query(models.User).filter(
        models.User.id == technician_id,
        models.User.role == "technician",
        models.User.is_active == True
    ).first()

    if not technician:
        raise HTTPException(status_code=400, detail="Invalid or inactive technician")

    ticket.assigned_to = technician.id
    ticket.status = "in_progress"

    db.commit()
    db.refresh(ticket)
    return ticket


# =========================
# UPDATE STATUS (STAFF ONLY)
# =========================
@router.put(
    "/{ticket_id}/status",
    response_model=schemas.TicketOut
)
def update_ticket_status(
    ticket_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    valid_statuses = ["open", "in_progress", "closed"]
    if status_value not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")

    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Técnicos solo sus asignados
    if current_user.role == "technician" and ticket.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this ticket")

    # Clientes bloqueados
    if current_user.role == "client":
        raise HTTPException(status_code=403, detail="Clients cannot modify ticket status")

    ticket.status = status_value
    db.commit()
    db.refresh(ticket)
    return ticket
