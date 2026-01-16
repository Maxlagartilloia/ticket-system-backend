from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importaciones sincronizadas con tu estructura física de archivos
from app.routers import (
    auth,
    usuarios,
    tickets,
    departments,
    equipment,
    instituciones,
    reportes,
)

# Generar tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"message": "CopierMaster API Online"}

# Esta ruta te dirá qué URLs reconoce el servidor realmente
@app.get("/check-routes")
def check_routes():
    return {"available_endpoints": [route.path for route in app.routes]}
