from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Ticket, Usuario
from app.dependencies import require_roles

router = APIRouter(prefix="/tickets", tags=["Tickets"])


# =========================
# CREAR TICKET
# =========================
@router.post("/", dependencies=[Depends(require_roles("admin", "cliente"))])
def crear_ticket(
    titulo: str,
    descripcion: Optional[str] = None,
    institucion_id: int = None,
    db: Session = Depends(get_db)
):
    if not institucion_id:
        raise HTTPException(status_code=400, detail="institucion_id es obligatorio")

    ticket = Ticket(
        titulo=titulo,
        descripcion=descripcion,
        institucion_id=institucion_id,
        estado="abierto"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


# =========================
# LISTAR TICKETS
# =========================
@router.get("/", dependencies=[Depends(require_roles("admin", "supervisor", "tecnico", "cliente"))])
def listar_tickets(
    rol: str,
    usuario_id: Optional[int] = None,
    institucion_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)

    if rol == "tecnico":
        if not usuario_id:
            raise HTTPException(status_code=400, detail="usuario_id requerido para técnico")
        query = query.filter(Ticket.tecnico_id == usuario_id)

    if rol == "cliente":
        if not institucion_id:
            raise HTTPException(status_code=400, detail="institucion_id requerido para cliente")
        query = query.filter(Ticket.institucion_id == institucion_id)

    return query.order_by(Ticket.created_at.desc()).all()


# =========================
# ASIGNAR / REASIGNAR TÉCNICO
# =========================
@router.put("/{ticket_id}/asignar", dependencies=[Depends(require_roles("admin", "supervisor"))])
def asignar_tecnico(
    ticket_id: int,
    tecnico_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    tecnico = db.query(Usuario).filter(Usuario.id == tecnico_id, Usuario.rol == "tecnico").first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no válido")

    ticket.tecnico_id = tecnico_id
    ticket.estado = "en_proceso"
    db.commit()
    db.refresh(ticket)
    return ticket


# =========================
# CERRAR TICKET
# =========================
@router.put("/{ticket_id}/cerrar", dependencies=[Depends(require_roles("admin", "supervisor", "tecnico"))])
def cerrar_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    ticket.estado = "cerrado"
    db.commit()
    db.refresh(ticket)
    return ticket


# =========================
# REABRIR TICKET
# =========================
@router.put("/{ticket_id}/reabrir", dependencies=[Depends(require_roles("admin", "supervisor"))])
def reabrir_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    ticket.estado = "abierto"
    db.commit()
    db.refresh(ticket)
    return ticket
