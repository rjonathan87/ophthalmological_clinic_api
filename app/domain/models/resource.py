from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    resource_type = Column(Enum("Room", "Equipment", name="resource_type"), nullable=False)
    location = Column(String(100))
    is_schedulable = Column(Boolean, nullable=False, default=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relaciones
    clinic = relationship("Clinic", back_populates="resources")
    created_by = relationship(
        "User", 
        foreign_keys=[created_by_user_id],
        backref="created_resources"
    )
    updated_by = relationship(
        "User", 
        foreign_keys=[updated_by_user_id],
        backref="updated_resources"
    )
    appointments = relationship("Appointment", back_populates="resource")