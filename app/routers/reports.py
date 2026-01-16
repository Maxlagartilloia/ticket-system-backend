from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database import get_db
from app import models, schemas
from app.dependencies import require_supervisor

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# =========================
# DASHBOARD STATS (SUPERVISOR / ADMIN)
# =========================
@router.get(
    "/dashboard",
    # Acoplado al esquema DashboardStats de schemas.py
    response_model=schemas.DashboardStats,
    dependencies=[Depends(require_supervisor)]
)
def dashboard_stats(
    db: Session = Depends(get_db)
):
    # Conteo de tickets abiertos
    open_tickets = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "open")
        .count()
    )

    # Conteo de tickets en progreso
    in_progress = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "in_progress")
        .count()
    )

    # Conteo de tickets resueltos hoy
    resolved_today = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.status == "closed",
            func.date(models.Ticket.updated_at) == date.today()
        )
        .count()
    )

    # Conteo de instituciones activas
    institutions_count = (
        db.query(models.Institution)
        .filter(models.Institution.is_active == True)
        .count()
    )

    return {
        "open_tickets": open_tickets,
        "in_progress": in_progress,
        "resolved_today": resolved_today,
        "institutions": institutions_count
    }
