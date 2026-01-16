from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import auth, users, tickets, institutions, departments, equipment, reports

# Crea las tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster API")

# 🛡️ CONFIGURACIÓN CORS BLINDADA
# Esto permite que tanto el dominio principal como el de soporte funcionen
origins = [
    "https://copiermastercyg.com.ec",
    "https://www.copiermastercyg.com.ec",
    "https://soporte.copiermastercyg.com.ec",
    "http://localhost:3000", # Para tus pruebas locales
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(institutions.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(tickets.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "CopierMaster Backend is Live and Secure"}
