import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importación absoluta para evitar errores de ruta en Render
from app.routers import auth, usuarios, tickets, departments, equipment, instituciones, reportes

# Intentar crear tablas
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creando tablas: {e}")

app = FastAPI(
    title="CopierMaster",
    docs_url="/docs",  # Forzamos la URL de documentación
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/test-v2")
def test():
    return {"status": "success", "info": "Si ves esto, el ruteo ya funciona"}

@app.get("/")
def read_root():
    return {"message": "Bienvenido a CopierMaster API"}
