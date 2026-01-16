from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔗 URL DE LA NUEVA BASE DE DATOS (Verificada de tu captura)
# Asegúrate de que no haya espacios al principio ni al final
SQLALCHEMY_DATABASE_URL = "postgresql://admin_copier:zmBhGep0NZcclyQR6C6YJQN1pcYy7b7t@dpg-d51bftre5dus73dlr8hg-a.ohio-postgres.render.com/copiermaster_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
