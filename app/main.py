from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import auth, users, tickets, institutions, departments, equipment, reports

# Crear tablas en la nueva DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(institutions.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(tickets.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"status": "V3 - Acceso Global Activado"}
