from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    auth,
    usuarios,
    instituciones,
    tickets,
    reportes,
    departments
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

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(instituciones.router, prefix="/instituciones", tags=["Instituciones"])
app.include_router(departments.router)
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "CopierMaster Backend",
        "version": "1.0.0"
    }
