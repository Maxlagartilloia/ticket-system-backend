from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# =========================
# USERS
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin | supervisor | technician | client
    is_active = Column(Boolean, default=True)

    tickets_created = relationship("Ticket", back_populates="created_by_user")
    tickets_assigned = relationship("Ticket", back_populates="assigned_technician")


# =========================
# INSTITUTIONS
# =========================
class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    is_active = Column(Boolean, default=True)

    departments = relationship("Department", back_populates="institution")
    tickets = relationship("Ticket", back_populates="institution")


# =========================
# DEPARTMENTS
# =========================
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)

    institution = relationship("Institution", back_populates="departments")
    equipment = relationship("Equipment", back_populates="department")


# =========================
# EQUIPMENT
# =========================
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    model = Column(String(255))
    serial_number = Column(String(255))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    department = relationship("Department", back_populates="equipment")
    tickets = relationship("Ticket", back_populates="equipment")


# =========================
# TICKETS
# =========================
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(50), nullable=False)  # low | medium | high
    status = Column(String(50), default="open")   # open | in_progress | closed

    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    institution = relationship("Institution", back_populates="tickets")
    equipment = relationship("Equipment", back_populates="tickets")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="tickets_created")
    assigned_technician = relationship("User", foreign_keys=[assigned_to], back_populates="tickets_assigned")
