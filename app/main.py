from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    auth,
    tickets,
    instituciones,
    usuarios,
    reportes,
)

# =========================
# DATABASE
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# APP
# =========================
app = FastAPI(
    title="CopierMaster – Sistema de Soporte",
    version="1.0.0"
)

# =========================
# CORS (FRONTEND)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://soporte.copiermastercyg.com.ec",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(instituciones.router, prefix="/instituciones", tags=["Instituciones"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"status": "CopierMaster API running"}
