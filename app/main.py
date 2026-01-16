from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importación de Routers corregida para coincidir con tus archivos en GitHub
from app.routers import (
    auth,
    usuarios,
    tickets,
    departments,  # Cambiado de 'departamentos' a 'departments'
    equipment,    # Asegúrate de que el archivo sea equipment.py
    instituciones,
    reportes,
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas (Routers)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router) # Referencia corregida
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"message": "CopierMaster API is running successfully"}
