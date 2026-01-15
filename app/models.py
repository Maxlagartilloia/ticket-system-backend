from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="supervisor")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String, nullable=False)
    equipment = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    technician = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
