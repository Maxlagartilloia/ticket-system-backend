from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, instituciones

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CopierMaster Ticket System API",
    version="1.0.0"
)

# CORS (para Netlify / frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(instituciones.router)


@app.get("/")
def root():
    return {"status": "OK", "service": "Ticket System Backend"}
