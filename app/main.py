from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth

app = FastAPI(
    title="CopierMaster Ticket System",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "Backend activo"}
