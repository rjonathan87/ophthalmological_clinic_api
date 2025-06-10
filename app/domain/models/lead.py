from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    lead_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    mobile_phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(150))
    age = Column(Integer)
    city = Column(String(80))
    service_id = Column(Integer, ForeignKey("services.id"))
    channel = Column(Enum("webchat", "whatsapp", "facebook", "instagram", "phone", "email", "website", "referral", name="channel_enum"), nullable=False)
    status = Column(Enum("new", "contacted", "scheduled", "lost", name="status_enum"), nullable=False, default="new")
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    service = relationship("Service", back_populates="leads")
    appointment = relationship("Appointment", back_populates="leads")
