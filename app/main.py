from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# Importaciones absolutas para garantizar el acoplamiento total
from app.routers.auth import router as auth_router
from app.routers.usuarios import router as usuarios_router
from app.routers.tickets import router as tickets_router
from app.routers.departments import router as departments_router
from app.routers.equipment import router as equipment_router
from app.routers.instituciones import router as instituciones_router
from app.routers.reportes import router as reportes_router

# Sincronizar tablas (confirmado con tu DBeaver)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CopierMaster API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas: Esto activa /auth/login, /usuarios, etc.
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(tickets_router)
app.include_router(departments_router)
app.include_router(equipment_router)
app.include_router(instituciones_router)
app.include_router(reportes_router)

@app.get("/")
def root():
    return {"status": "online", "message": "Backend de CopierMaster operando"}
