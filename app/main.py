from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users, tickets, equipment, institutions, departments

# ==========================================
# DATABASE INITIALIZATION (Render Auto-Sync)
# ==========================================
# Esto crea las tablas en PostgreSQL si no existen al arrancar
Base.metadata.create_all(bind=engine)

# ==========================================
# APP CONFIGURATION
# ==========================================
app = FastAPI(
    title="CopierMaster API",
    description="Professional Ticketing System for Technical Services",
    version="1.0.0"
)

# Configuración de CORS para permitir que el Frontend se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ROUTER REGISTRATION
# ==========================================
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(institutions.router)
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
app.include_router(equipment.router)
app.include_router(tickets.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "CopierMaster API",
        "environment": "Production/Render"
    }
