from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ConsentForm(Base):
    __tablename__ = "consentforms"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    
    form_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    signature_data = Column(JSON)  # Para almacenar datos de firma digital si es necesario
    signed_date = Column(DateTime)
    status = Column(String(50), nullable=False, default='Pending')  # Pending, Signed, Rejected, Expired
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(String(20), nullable=False)
    
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    signed_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    patient = relationship("Patient", back_populates="consent_forms")
    clinic = relationship("Clinic", back_populates="consent_forms")
    consultation = relationship("Consultation", back_populates="consent_forms")
    appointment = relationship("Appointment", back_populates="consent_forms")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_consent_forms")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_consent_forms")
    signed_by_user = relationship("User", foreign_keys=[signed_by_user_id], back_populates="signed_consent_forms")
