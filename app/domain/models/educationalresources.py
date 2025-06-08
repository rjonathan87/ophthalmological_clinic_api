from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship

class EducationalResource(Base):
    __tablename__ = "educational_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content_type = Column(Enum('Article', 'Video', 'PDF', 'Interactive', name='content_type'), nullable=False)
    content_url = Column(String(512))
    description = Column(Text)
    category = Column(String(100))
    tags = Column(JSON)
    language = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    patient_trackings = relationship("PatientEducationTracking", back_populates="resource")