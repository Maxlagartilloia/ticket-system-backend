from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importaciones sincronizadas con tu GitHub
from app.routers import (
    auth,
    usuarios,
    tickets,
    departments,
    equipment,
    instituciones,
    reportes,
)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers - ASEGÚRATE DE QUE QUEDEN ASÍ
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"message": "API de CopierMaster Online"}

@app.get("/debug-routes")
def debug():
    return {"routes": [route.path for route in app.routes]}
