from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date
import io
import pandas as pd

from app.database import get_db
from app.models import Ticket, Institucion
from app.dependencies import require_roles

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

router = APIRouter(prefix="/reportes", tags=["Reportes"])


# =========================
# REPORTE CSV POR INSTITUCIÓN
# =========================
@router.get(
    "/tickets/csv",
    dependencies=[Depends(require_roles("admin", "supervisor"))]
)
def reporte_tickets_csv(
    institucion_id: int,
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    institucion = db.query(Institucion).filter(
        Institucion.id == institucion_id
    ).first()

    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")

    tickets = db.query(Ticket).filter(
        Ticket.institucion_id == institucion_id,
        Ticket.created_at >= fecha_inicio,
        Ticket.created_at <= fecha_fin
    ).all()

    data = []
    for t in tickets:
        data.append({
            "ID": t.id,
            "Título": t.titulo,
            "Estado": t.estado,
            "Técnico ID": t.tecnico_id,
            "Fecha": t.created_at.strftime("%Y-%m-%d %H:%M")
        })

    df = pd.DataFrame(data)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=reporte_tickets_{institucion.nombre}.csv"
        }
    )


# =========================
# REPORTE PDF POR INSTITUCIÓN
# =========================
@router.get(
    "/tickets/pdf",
    dependencies=[Depends(require_roles("admin", "supervisor"))]
)
def reporte_tickets_pdf(
    institucion_id: int,
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    institucion = db.query(Institucion).filter(
        Institucion.id == institucion_id
    ).first()

    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")

    tickets = db.query(Ticket).filter(
        Ticket.institucion_id == institucion_id,
        Ticket.created_at >= fecha_inicio,
        Ticket.created_at <= fecha_fin
    ).all()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "REPORTE DE TICKETS")
    y -= 25

    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Institución: {institucion.nombre}")
    y -= 15
    pdf.drawString(40, y, f"Periodo: {fecha_inicio} a {fecha_fin}")
    y -= 25

    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(40, y, "ID")
    pdf.drawString(80, y, "TÍTULO")
    pdf.drawString(300, y, "ESTADO")
    pdf.drawString(380, y, "TÉCNICO")
    pdf.drawString(450, y, "FECHA")
    y -= 10

    pdf.setFont("Helvetica", 9)

    for t in tickets:
        if y < 50:
            pdf.showPage()
            y = height - 40
            pdf.setFont("Helvetica", 9)

        pdf.drawString(40, y, str(t.id))
        pdf.drawString(80, y, t.titulo[:30])
        pdf.drawString(300, y, t.estado)
        pdf.drawString(380, y, str(t.tecnico_id or "N/A"))
        pdf.drawString(450, y, t.created_at.strftime("%Y-%m-%d"))
        y -= 12

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=reporte_tickets_{institucion.nombre}.pdf"
        }
    )
