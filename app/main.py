from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importaciones corregidas y acopladas a tu estructura de archivos en GitHub
from app.routers import (
    auth,
    usuarios,
    tickets,
    departments,  # Acoplado a app/routers/departments.py
    equipment,    # Acoplado a app/routers/equipment.py
    instituciones,
    reportes,
)

# Crear tablas en la base de datos al iniciar la aplicación
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

# Configuración de CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers (Rutas de la API)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "CopierMaster API funcionando correctamente",
        "version": "1.0.0"
    }
