from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get(
    "/dashboard",
    response_model=schemas.DashboardStats
)
def dashboard_stats(db: Session = Depends(get_db)):
    open_tickets = db.query(models.Ticket).filter(models.Ticket.status == "open").count()
    in_progress = db.query(models.Ticket).filter(models.Ticket.status == "in_progress").count()
    resolved_today = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.status == "closed",
            func.date(models.Ticket.updated_at) == date.today()
        )
        .count()
    )
    institutions = db.query(models.Institution).count()

    return {
        "open_tickets": open_tickets,
        "in_progress": in_progress,
        "resolved_today": resolved_today,
        "institutions": institutions
    }
