from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔗 URL DE LA NUEVA BASE DE DATOS (VIRGINIA)
# Datos extraídos de tu captura {676F8420-E2D2-4B8E-87A7-D40BDEF41334}.png
SQLALCHEMY_DATABASE_URL = "postgresql://admin_copier:Ympx3MrbMYKtV9axG9GRN3N8tqfmjTYI@dpg-d51bpe3e5dus73dm20eg-a.virginia-postgres.render.com/copiermaster_db_v64q"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
