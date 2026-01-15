from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=schemas.TicketOut)
def crear_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    nuevo = models.Ticket(**ticket.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=list[schemas.TicketOut])
def listar_tickets(db: Session = Depends(get_db)):
    return db.query(models.Ticket).all()


@router.put("/{ticket_id}", response_model=schemas.TicketOut)
def actualizar_ticket(ticket_id: int, data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if data.estado:
        ticket.estado = data.estado
    if data.tecnico_id:
        ticket.tecnico_id = data.tecnico_id

    db.commit()
    db.refresh(ticket)
    return ticket
