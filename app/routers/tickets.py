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
    # Validar institución existente y activa
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

    equipment_id = None

    # Validar equipment si se envía
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

        # Validar que el equipment pertenezca a la institución
        department = (
            db.query(models.Department)
            .filter(models.Department.id == equipment.department_id)
            .first()
        )

        if not department or department.institution_id != institution.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Equipment does not belong to institution"
            )

        equipment_id = equipment.id

    ticket = models.Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status="open",
        institution_id=payload.institution_id,
        equipment_id=equipment_id,
        created_by=current_user.id,
        assigned_to=None
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


# =========================
# LIST TICKETS (ROLE-BASED)
# =========================
@router.get(
    "/",
    response_model=List[schemas.TicketOut]
)
def list_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role in ["admin", "supervisor"]:
        return (
            db.query(models.Ticket)
            .order_by(models.Ticket.created_at.desc())
            .all()
        )

    if current_user.role == "technician":
        return (
            db.query(models.Ticket)
            .filter(models.Ticket.assigned_to == current_user.id)
            .order_by(models.Ticket.created_at.desc())
            .all()
        )

    # client
    return (
        db.query(models.Ticket)
        .filter(models.Ticket.created_by == current_user.id)
        .order_by(models.Ticket.created_at.desc())
        .all()
    )


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
    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if ticket.status != "open":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only open tickets can be assigned"
        )

    technician = (
        db.query(models.User)
        .filter(
            models.User.id == technician_id,
            models.User.role == "technician",
            models.User.is_active == True
        )
        .first()
    )

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid technician"
        )

    ticket.assigned_to = technician.id
    ticket.status = "in_progress"

    db.commit()
    db.refresh(ticket)

    return ticket


# =========================
# UPDATE TICKET STATUS
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
    if status_value not in ["open", "in_progress", "closed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )

    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    # Technician solo puede cambiar estado si es el asignado
    if current_user.role == "technician":
        if ticket.assigned_to != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )

    if current_user.role not in ["admin", "supervisor", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    ticket.status = status_value
    db.commit()
    db.refresh(ticket)

    return ticket
