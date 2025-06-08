from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PatientEducationTracking(Base):
    __tablename__ = "patient_education_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("educational_resources.id"), nullable=False)
    status = Column(String(50), nullable=False, default='Assigned')  # Assigned, InProgress, Completed
    progress = Column(Integer, default=0)  # Porcentaje de progreso
    feedback = Column(Text)  # Comentarios del paciente
    quiz_results = Column(JSON)  # Resultados de evaluaciones si aplica
    notes = Column(Text)  # Notas del personal médico
    completion_date = Column(DateTime)
    
    # Campos de auditoría
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    patient = relationship("Patient", back_populates="education_trackings")
    resource = relationship("EducationalResource", back_populates="patient_trackings")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_education_trackings")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_education_trackings")
