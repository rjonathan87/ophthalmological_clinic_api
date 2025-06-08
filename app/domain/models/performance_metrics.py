from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Date, Enum, Text
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class PerformanceMetrics(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Numeric(10,2), nullable=False)
    metric_target = Column(Numeric(10,2))
    measurement_date = Column(Date, nullable=False)
    metric_category = Column(Enum('Clinical', 'Financial', 'Operational', 'Patient Satisfaction'), nullable=False)
    description = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime(timezone=True))
