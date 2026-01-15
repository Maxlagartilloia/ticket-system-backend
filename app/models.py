from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Institucion(Base):
    __tablename__ = "instituciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    contrato = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("Usuario", back_populates="institucion")
    tickets = relationship("Ticket", back_populates="institucion")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # admin, supervisor, tecnico, cliente
    institucion_id = Column(Integer, ForeignKey("instituciones.id"), nullable=True)

    institucion = relationship("Institucion", back_populates="usuarios")
    tickets = relationship("Ticket", back_populates="tecnico")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    estado = Column(String, default="abierto")
    institucion_id = Column(Integer, ForeignKey("instituciones.id"))
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    institucion = relationship("Institucion", back_populates="tickets")
    tecnico = relationship("Usuario", back_populates="tickets")
