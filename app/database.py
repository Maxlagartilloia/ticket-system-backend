from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

# Enumerations for strict status and roles
class UserRole(str, enum.Enum):
    admin = "admin"
    technician = "technician"

class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)

    # Relationships
    users = relationship("User", back_populates="institution")
    tickets = relationship("Ticket", back_populates="institution")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="technician") # 'admin' or 'technician'
    is_active = Column(Boolean, default=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"))

    # Relationships
    institution = relationship("Institution", back_populates="users")
    created_tickets = relationship("Ticket", back_populates="creator")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="open") # 'open', 'in_progress', 'closed'
    priority = Column(String, default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"))
    institution_id = Column(Integer, ForeignKey("institutions.id"))

    # Relationships
    creator = relationship("User", back_populates="created_tickets")
    institution = relationship("Institution", back_populates="tickets")
