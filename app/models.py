from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# =========================
# USERS
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin | supervisor | technician | client

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    assigned_tickets = relationship("Ticket", back_populates="technician")


# =========================
# INSTITUTIONS
# =========================

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    departments = relationship(
        "Department",
        back_populates="institution",
        cascade="all, delete-orphan"
    )


# =========================
# DEPARTMENTS
# =========================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    institution_id = Column(
        Integer,
        ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False
    )

    institution = relationship("Institution", back_populates="departments")

    equipments = relationship(
        "Equipment",
        back_populates="department",
        cascade="all, delete-orphan"
    )


# =========================
# EQUIPMENT
# =========================

class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    serial_number = Column(String, nullable=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False
    )

    department = relationship("Department", back_populates="equipments")

    tickets = relationship("Ticket", back_populates="equipment")


# =========================
# TICKETS
# =========================

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    priority = Column(String, default="medium")  # low | medium | high
    status = Column(String, default="open")      # open | in_progress | closed

    institution_id = Column(
        Integer,
        ForeignKey("institutions.id"),
        nullable=False
    )

    equipment_id = Column(
        Integer,
        ForeignKey("equipments.id"),
        nullable=False
    )

    technician_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    institution = relationship("Institution")
    equipment = relationship("Equipment", back_populates="tickets")
    technician = relationship("User", back_populates="assigned_tickets")
