from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    auth,
    usuarios,
    instituciones,
    departments,
    equipment,
    tickets,
    reportes
)

# =========================
# DATABASE INIT
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="CopierMaster Ticket System",
    version="1.0.0"
)

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego se restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(instituciones.router, prefix="/instituciones", tags=["Institutions"])
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
app.include_router(equipment.router, prefix="/equipment", tags=["Equipment"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(reportes.router, prefix="/reportes", tags=["Reports"])

# =========================
# HEALTHCHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "CopierMaster Backend",
        "version": "1.0.0"
    }
