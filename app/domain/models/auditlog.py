from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class AuditLog(Base):
    __tablename__ = "auditlogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    action_type = Column(String(100), nullable=False)  # e.g., 'CREATE', 'UPDATE', 'DELETE', 'LOGIN'
    entity_type = Column(String(100))  # e.g., 'Patient', 'Appointment', 'User'
    entity_id = Column(String(100))  # String to support various ID formats
    details = Column(Text)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    severity = Column(String(50))  # e.g., 'Low', 'Medium', 'High', 'Critical'
    related_records = Column(JSON)  # For storing related record IDs
    system_component = Column(String(100))  # e.g., 'Authentication', 'Patient Management'
    is_reviewed = Column(Boolean, default=False)
    reviewed_by_user_id = Column(Integer, ForeignKey("users.id"))
    review_notes = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    reviewed_at = Column(DateTime)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="audit_logs")
    clinic = relationship("Clinic", back_populates="audit_logs")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by_user_id], backref="reviewed_audit_logs")
