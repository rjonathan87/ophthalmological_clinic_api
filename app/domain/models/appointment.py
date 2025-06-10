from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    appointment_type = Column(String(100))
    status = Column(String(50), nullable=False)
    reason_for_visit = Column(Text)
    cancellation_reason = Column(Text)
    confirmation_sent_at = Column(DateTime)
    reminder_sent_at = Column(DateTime)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    primary_doctor_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    # Relaciones
    clinic = relationship("Clinic", back_populates="appointments")
    primary_doctor = relationship("User", foreign_keys=[primary_doctor_id], back_populates="primary_doctor_appointments")
    patient = relationship("Patient", back_populates="appointments")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_appointments")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_appointments")
    appointment_services = relationship("AppointmentService", back_populates="appointment")    
    resource = relationship("Resource", back_populates="appointments")    
    consultations = relationship("Consultation", back_populates="appointment")
    consent_forms = relationship("ConsentForm", back_populates="appointment")
    invoices = relationship("Invoice", back_populates="appointment")
    leads = relationship("Lead", back_populates="appointment")
