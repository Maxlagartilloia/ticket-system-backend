from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app import models, schemas
from app.dependencies import require_supervisor

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# =========================
# DASHBOARD METRICS
# =========================
@router.get(
    "/dashboard",
    response_model=schemas.DashboardStats
)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_supervisor)
):
    open_tickets = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "open")
        .count()
    )

    in_progress = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "in_progress")
        .count()
    )

    resolved_today = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.status == "closed",
            models.Ticket.updated_at >= date.today()
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
