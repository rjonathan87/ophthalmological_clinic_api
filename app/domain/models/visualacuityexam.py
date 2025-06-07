from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class VisualAcuityExam(Base):
    __tablename__ = "visualacuityexams"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"), nullable=False)
    exam_date = Column(DateTime, nullable=False, default=func.now())
    
    # Mediciones de agudeza visual sin corrección
    uncorrected_va_od = Column(String(10))  # Ojo derecho sin corrección
    uncorrected_va_os = Column(String(10))  # Ojo izquierdo sin corrección
    
    # Mediciones de agudeza visual con corrección actual
    current_correction_va_od = Column(String(10))  # Ojo derecho con corrección actual
    current_correction_va_os = Column(String(10))  # Ojo izquierdo con corrección actual
    
    # Mediciones de agudeza visual con nueva corrección
    new_correction_va_od = Column(String(10))  # Ojo derecho con nueva corrección
    new_correction_va_os = Column(String(10))  # Ojo izquierdo con nueva corrección
    
    # Método de medición y condiciones
    test_method = Column(String(50))  # Ej: Snellen, LogMAR, etc.
    test_distance = Column(Float)  # Distancia del test en metros
    lighting_conditions = Column(String(50))  # Condiciones de iluminación
    
    notes = Column(Text)  # Notas adicionales
    exam_data = Column(JSON)  # Datos adicionales del examen en formato JSON
    
    # Campos de auditoría
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    consultation = relationship("Consultation", back_populates="visualacuityexams")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_visualacuityexams")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_visualacuityexams")
