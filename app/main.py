from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.routers import auth, users, tickets, institutions, departments, equipment, reports

app = FastAPI(title="CopierMaster API")

# 🔒 Configuración de Seguridad para Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://soporte.copiermastercyg.com.ec", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas del Sistema
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(institutions.router)
app.include_router(departments.router)
app.include_router(equipment.router)
app.include_router(tickets.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"status": "Sistema Online - Conectado a Supabase"}
