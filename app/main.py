from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importación directa y segura
import app.routers.auth as auth
import app.routers.usuarios as usuarios
import app.routers.tickets as tickets
import app.routers.departments as departments
import app.routers.equipment as equipment
import app.routers.instituciones as instituciones
import app.routers.reportes as reportes

# Crear tablas en la DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster Ticket System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas con prefijos manuales para seguridad total
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(instituciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"message": "API Online"}
