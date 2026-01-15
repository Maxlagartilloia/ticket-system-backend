from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Ticket
from schemas import TicketCreate, TicketResponse

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(
        institution=ticket.institution,
        equipment=ticket.equipment,
        description=ticket.description,
        priority=ticket.priority
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()
