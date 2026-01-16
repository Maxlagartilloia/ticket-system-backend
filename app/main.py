from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    auth,
    usuarios,
    tickets,
    departamentos,
    equipment,
    instituciones,
    reportes,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departamentos.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)
