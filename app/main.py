from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importaciones forzadas para asegurar el acoplamiento
from app.routers import (
    auth,
    usuarios,
    tickets,
    departments,
    equipment,
    instituciones,
    reportes
)

# Crear tablas en la DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CopierMaster Ticket System",
    description="Sistema de gestión de tickets - API Backend",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro explícito de rutas
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/", tags=["Root"])
def root():
    return {"status": "online", "message": "CopierMaster API Ready"}

# Ruta de diagnóstico para ingenieros
@app.get("/debug-urls", tags=["Debug"])
def debug_urls():
    return {"urls": [route.path for route in app.routes]}
