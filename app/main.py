from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
# Importamos los modelos para que Base los conozca antes de crear las tablas
from app import models
from app.routers import auth, users, tickets, institutions, departments, equipment, reports

# Crea las tablas en la base de datos de Render
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster API")

# Configuración de CORS para tu dominio de Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://copiermastercyg.com.ec", "http://localhost:3000"],
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
    return {"message": "CopierMaster Backend is Live"}
