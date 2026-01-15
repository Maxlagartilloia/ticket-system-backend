from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # admin | supervisor | tecnico | cliente
    institucion_id = Column(Integer, nullable=True)


class Institucion(Base):
    __tablename__ = "instituciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    contrato = Column(String, nullable=False)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    estado = Column(String, default="abierto")
    prioridad = Column(String)
    institucion_id = Column(Integer, ForeignKey("instituciones.id"))
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HistorialTicket(Base):
    __tablename__ = "historial_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    accion = Column(String)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
