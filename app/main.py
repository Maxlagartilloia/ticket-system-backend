from fastapi import FastAPI
from app.database import Base, engine
from app.routers import instituciones

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CopierMaster Ticket System",
    version="1.0.0"
)

app.include_router(instituciones.router)


@app.get("/")
def health():
    return {"status": "OK", "backend": "CopierMaster Tickets"}
