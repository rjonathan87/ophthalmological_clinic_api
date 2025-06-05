from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime)

    clinic = relationship("Clinic", back_populates="resources")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_resources")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_resources")
