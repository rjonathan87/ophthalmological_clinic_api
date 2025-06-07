from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class Clinic(Base):
    __tablename__ = "clinics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(Text)
    phone_number = Column(String(30))
    email = Column(String(100))
    website = Column(String(255))
    timezone = Column(String(50), nullable=False, default='UTC')
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    # Relaciones
    users = relationship("User", back_populates="clinic")
    patients = relationship("Patient", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")
    resources = relationship("Resource", back_populates="clinic")
    services = relationship("Service", back_populates="clinic")
    audit_logs = relationship("AuditLog", back_populates="clinic")
    clinical_studies = relationship("ClinicalStudy", back_populates="clinic")
    resources = relationship("Resource", back_populates="clinic", cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="clinic")  # Nueva relación
