from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class ClinicalStudy(Base):
    __tablename__ = "clinical_studies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    study_type = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    status = Column(String(50), nullable=False)
    protocol_id = Column(Integer, ForeignKey("clinical_protocols.id"))
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime)

    protocol = relationship("ClinicalProtocol", back_populates="studies")
    clinic = relationship("Clinic", back_populates="clinical_studies")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id])
