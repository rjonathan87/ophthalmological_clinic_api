from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON

class PatientDocument(Base):
    __tablename__ = "patientdocuments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer)
    upload_date = Column(DateTime, nullable=False, server_default=func.now())
    document_date = Column(DateTime, nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default='Active')
    is_private = Column(Boolean, default=False)
    document_metadata = Column(JSON)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    patient = relationship("Patient", back_populates="documents")
    clinic = relationship("Clinic", back_populates="patient_documents")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_documents")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_documents")
