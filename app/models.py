from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    rol = Column(String, nullable=False)  # admin | supervisor | tecnico

    tickets_asignados = relationship("Ticket", back_populates="tecnico")


class Institucion(Base):
    __tablename__ = "instituciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    tickets = relationship("Ticket", back_populates="institucion")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    prioridad = Column(String, default="baja")
    estado = Column(String, default="abierto")

    institucion_id = Column(Integer, ForeignKey("instituciones.id"))
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    institucion = relationship("Institucion", back_populates="tickets")
    tecnico = relationship("Usuario", back_populates="tickets_asignados")
