from fastapi import FastAPI
from app.database import Base, engine
from app.routers import instituciones, usuarios, tickets, reportes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CopierMaster Ticket System",
    version="1.0.0"
)

app.include_router(instituciones.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(reportes.router)


@app.get("/")
def health():
    return {
        "status": "OK",
        "service": "CopierMaster Tickets Backend"
    }
