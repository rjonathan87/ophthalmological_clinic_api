from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    consultation_date = Column(DateTime, nullable=False, default=func.now())
    chief_complaint = Column(Text, nullable=False)
    notes = Column(Text)
    consultation_type = Column(String(50))
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    follow_up_date = Column(DateTime)
    consultation_status = Column(String(50), nullable=False, default='Completed')
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    appointment = relationship("Appointment", back_populates="consultations")
    patient = relationship("Patient", back_populates="consultations")
    clinic = relationship("Clinic", back_populates="consultations")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="doctor_consultations")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_consultations")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_consultations")
    prescriptions = relationship("Prescription", back_populates="consultation", cascade="all, delete-orphan")
    refractionexams = relationship("RefractionExam", back_populates="consultation", cascade="all, delete-orphan")
    visualacuityexams = relationship("VisualAcuityExam", back_populates="consultation", cascade="all, delete-orphan")
    iopexams = relationship("IOPExam", back_populates="consultation", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="consultation")
