from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

# =========================
# CREATE TICKET
# =========================
@router.post(
    "/",
    response_model=schemas.TicketOut,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_ticket = models.Ticket(
        title="Support Ticket",
        description=ticket.description,
        priority=ticket.priority,
        status="open",
        institution_id=ticket.institution_id,
        equipment_id=None,
        created_by=current_user.id,
        assigned_to=None
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# =========================
# LIST ALL TICKETS
# =========================
@router.get(
    "/",
    response_model=List[schemas.TicketOut]
)
def list_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Admin & Supervisor see all tickets
    if current_user.role in ["admin", "supervisor"]:
        return db.query(models.Ticket).order_by(models.Ticket.created_at.desc()).all()

    # Technicians see only assigned tickets
    if current_user.role == "technician":
        return (
            db.query(models.Ticket)
            .filter(models.Ticket.assigned_to == current_user.id)
            .order_by(models.Ticket.created_at.desc())
            .all()
        )

    # Clients see only their own tickets
    return (
        db.query(models.Ticket)
        .filter(models.Ticket.created_by == current_user.id)
        .order_by(models.Ticket.created_at.desc())
        .all()
    )


# =========================
# UPDATE TICKET
# =========================
@router.put(
    "/{ticket_id}",
    response_model=schemas.TicketOut
)
def update_ticket(
    ticket_id: int,
    data: schemas.TicketUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
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

    # Only admin or supervisor can reassign or close tickets
    if current_user.role not in ["admin", "supervisor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    if data.status is not None:
        ticket.status = data.status

    if data.priority is not None:
        ticket.priority = data.priority

    if data.technician_id is not None:
        ticket.assigned_to = data.technician_id

    db.commit()
    db.refresh(ticket)

    return ticket
