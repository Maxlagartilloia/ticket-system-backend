import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔒 SEGURIDAD TOTAL: 
# Extraemos la conexión de las variables de entorno. 
# En Supabase la encontrarás como "Connection String" (URI).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Verificación para asegurar que la app no arranque a ciegas
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("ERROR: No se encontró la variable DATABASE_URL. Configúrala en tu plataforma de despliegue.")

# Optimizamos la conexión para Supabase (PostgreSQL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica que la conexión esté viva antes de usarla
    pool_recycle=3600    # Recicla conexiones cada hora para evitar cortes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para los routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
