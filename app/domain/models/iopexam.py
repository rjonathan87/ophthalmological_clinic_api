from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class IOPExam(Base):
    __tablename__ = "iopexams"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"), nullable=False)
    exam_date = Column(DateTime, nullable=False, default=func.now())
    pressure_od = Column(Float)  # Presión intraocular ojo derecho
    pressure_os = Column(Float)  # Presión intraocular ojo izquierdo
    measurement_method = Column(String(50))  # Método de medición (ej: Tonometría de Goldmann, etc.)
    time_of_day = Column(String(20))  # Momento del día de la medición
    medication_used = Column(String(255))  # Medicamentos utilizados antes de la medición
    notes = Column(Text)  # Notas adicionales
    exam_data = Column(JSON)  # Datos adicionales del examen en formato JSON
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    consultation = relationship("Consultation", back_populates="iopexams")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_iopexams")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_iopexams")
