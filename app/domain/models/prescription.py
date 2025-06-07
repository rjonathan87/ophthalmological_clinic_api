from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    prescribed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prescription_date = Column(DateTime, nullable=False, default=func.now())
    prescription_type = Column(String(50), nullable=False)  # e.g., 'Medication', 'Optical', 'Contact Lens'
    prescription_details = Column(JSON)  # Stored as JSON for flexibility
    instructions = Column(Text)
    expiration_date = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    consultation = relationship("Consultation", back_populates="prescriptions")
    patient = relationship("Patient", back_populates="prescriptions")
    prescribed_by = relationship("User", foreign_keys=[prescribed_by_id], back_populates="prescribed_prescriptions")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_prescriptions")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_prescriptions")
