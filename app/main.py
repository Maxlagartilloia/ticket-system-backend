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

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CopierMaster Ticket System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS
app.include_router(auth.router)
app.include_router(usuarios.router, prefix="/usuarios")
app.include_router(instituciones.router, prefix="/instituciones")
app.include_router(departments.router, prefix="/departments")
app.include_router(equipment.router, prefix="/equipment")
app.include_router(tickets.router, prefix="/tickets")
app.include_router(reportes.router, prefix="/reportes")

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "CopierMaster Backend",
        "version": "1.0.0"
    }
