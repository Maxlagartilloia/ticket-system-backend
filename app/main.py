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
# auth, usuarios y tickets YA tienen prefijo en su router
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)

# estos routers NO tienen prefijo interno
app.include_router(instituciones.router, prefix="/instituciones")
app.include_router(departments.router, prefix="/departments")
app.include_router(equipment.router, prefix="/equipment")
app.include_router(reportes.router, prefix="/reportes")

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
