from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class RefractionExam(Base):
    __tablename__ = "refractionexams"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"), nullable=False)
    exam_date = Column(DateTime, nullable=False, default=func.now())
    sphere_od = Column(Float)  # Esfera ojo derecho
    cylinder_od = Column(Float)  # Cilindro ojo derecho
    axis_od = Column(Integer)  # Eje ojo derecho
    va_od = Column(String(10))  # Agudeza visual ojo derecho
    sphere_os = Column(Float)  # Esfera ojo izquierdo
    cylinder_os = Column(Float)  # Cilindro ojo izquierdo
    axis_os = Column(Integer)  # Eje ojo izquierdo
    va_os = Column(String(10))  # Agudeza visual ojo izquierdo
    addition = Column(Float)  # Adición para lectura cercana
    ipd = Column(Float)  # Distancia interpupilar
    notes = Column(Text)  # Notas adicionales
    exam_data = Column(JSON)  # Datos adicionales del examen en formato JSON
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    consultation = relationship("Consultation", back_populates="refractionexams")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_refractionexams")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_refractionexams")
