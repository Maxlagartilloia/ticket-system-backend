from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importaciones sincronizadas con tu estructura real de archivos
from app.routers import (
    auth,
    usuarios,
    tickets,
    departments,  # Sincronizado con departments.py
    equipment,    # Sincronizado con equipment.py
    instituciones,
    reportes,
)

# Generar tablas en la DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas corregido
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"status": "online", "message": "CopierMaster API Funcionando"}
