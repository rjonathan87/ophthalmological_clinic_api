from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    patient_identifier = Column(String(50), unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other', 'PreferNotToSay', name='gender_enum'))
    address = Column(Text)
    phone_number = Column(String(30))
    email = Column(String(100))
    emergency_contact_name = Column(String(150))
    emergency_contact_phone = Column(String(30))
    primary_care_physician = Column(String(150))
    insurance_provider = Column(String(100))
    insurance_policy_number = Column(String(100))
    medical_history_summary = Column(Text)
    allergies = Column(Text)
    preferred_communication_channel = Column(Enum('Email', 'SMS', 'Phone', 'Portal', name='communication_channel_enum'))
    gdpr_consent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    clinic = relationship("Clinic", back_populates="patients")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_patients")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_patients")
    user_account = relationship("User", foreign_keys=[user_id], back_populates="patient_user")
    appointments = relationship("Appointment", back_populates="patient")
    consultations = relationship("Consultation", back_populates="patient")  # Nueva relación

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
