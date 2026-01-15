from fastapi import FastAPI
from app.database import Base, engine
from app.routers import instituciones, tickets

# Crear tablas (si faltan)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CopierMaster Ticket System",
    version="1.0.0"
)

# Routers
app.include_router(instituciones.router)
app.include_router(tickets.router)


@app.get("/")
def health():
    return {"status": "OK", "service": "CopierMaster Tickets Backend"}
