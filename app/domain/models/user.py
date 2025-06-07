from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class User(Base):
    __allow_unmapped__ = True
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(30))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    associated_clinic_id = Column(Integer, ForeignKey("clinics.id"))
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relaciones
    role = relationship("Role", back_populates="users")
    clinic = relationship("Clinic", back_populates="users")
    created_appointments = relationship("Appointment", foreign_keys="Appointment.created_by_user_id", back_populates="created_by_user")
    updated_appointments = relationship("Appointment", foreign_keys="Appointment.updated_by_user_id", back_populates="updated_by_user")
    primary_doctor_appointments = relationship("Appointment", foreign_keys="Appointment.primary_doctor_id", back_populates="primary_doctor")
    created_patients = relationship("Patient", foreign_keys="[Patient.created_by_user_id]", back_populates="created_by_user")
    updated_patients = relationship("Patient", foreign_keys="[Patient.updated_by_user_id]", back_populates="updated_by_user")
    patient_user = relationship("Patient", foreign_keys="[Patient.user_id]", back_populates="user_account")
    created_services = relationship("Service", foreign_keys="[Service.created_by_user_id]", back_populates="created_by_user")
    updated_services = relationship("Service", foreign_keys="[Service.updated_by_user_id]", back_populates="updated_by_user")
    doctor_consultations = relationship("Consultation", foreign_keys="[Consultation.doctor_id]", back_populates="doctor")
    created_consultations = relationship("Consultation", foreign_keys="[Consultation.created_by_user_id]", back_populates="created_by_user")
    updated_consultations = relationship("Consultation", foreign_keys="[Consultation.updated_by_user_id]", back_populates="updated_by_user")
    prescribed_prescriptions = relationship("Prescription", foreign_keys="[Prescription.prescribed_by_id]", back_populates="prescribed_by")
    created_prescriptions = relationship("Prescription", foreign_keys="[Prescription.created_by_user_id]", back_populates="created_by_user")
    updated_prescriptions = relationship("Prescription", foreign_keys="[Prescription.updated_by_user_id]", back_populates="updated_by_user")
    created_refractionexams = relationship("RefractionExam", foreign_keys="[RefractionExam.created_by_user_id]", back_populates="created_by_user")
    updated_refractionexams = relationship("RefractionExam", foreign_keys="[RefractionExam.updated_by_user_id]", back_populates="updated_by_user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
