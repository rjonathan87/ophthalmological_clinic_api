from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON
from typing import List, Optional

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    notes = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    primary_doctor_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    clinic = relationship("Clinic", back_populates="appointments")
    primary_doctor = relationship("User", foreign_keys=[primary_doctor_id], back_populates="primary_doctor_appointments")
    patient = relationship("Patient", back_populates="appointments")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_appointments")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_appointments")
    appointment_services = relationship("AppointmentService", back_populates="appointment")

class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(Text)
    phone_number = Column(String(30))
    email = Column(String(100))
    website = Column(String(255))
    timezone = Column(String(50), nullable=False, default='UTC')
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    users = relationship("User", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")
    patients = relationship("Patient", back_populates="clinic")
    resources = relationship("Resource", back_populates="clinic")
    services = relationship("Service", back_populates="clinic")
    studies = relationship("ClinicalStudy", back_populates="clinic")

    def __repr__(self):
        return f"<Clinic(name='{self.name}')>"

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    role_permissions = relationship("RolePermission", back_populates="permission")

    def __repr__(self):
        return f"<Permission(name='{self.name}')>"

class RolePermission(Base):
    __tablename__ = "rolepermissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")

    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")

    @property
    def permissions(self):
        return [rp.permission for rp in self.role_permissions]

    def __repr__(self):
        return f"<Role(name='{self.name}')>"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100))
    entity_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", foreign_keys=[user_id])

class ClinicalProtocol(Base):
    __tablename__ = "clinical_protocols"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    protocol_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime)

    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id])
    studies = relationship("ClinicalStudy", back_populates="protocol")

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
    clinic = relationship("Clinic", back_populates="studies")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id])

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

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime)

    clinic = relationship("Clinic", back_populates="services")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_services")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_services")
    appointment_services = relationship("AppointmentService", back_populates="service")

class AppointmentService(Base):
    __tablename__ = "appointment_services"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime)

    appointment = relationship("Appointment", back_populates="appointment_services")
    service = relationship("Service", back_populates="appointment_services")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id])

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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

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

    role = relationship("Role", back_populates="users")
    clinic = relationship("Clinic", back_populates="users")
    created_appointments = relationship("Appointment", foreign_keys="Appointment.created_by_user_id", back_populates="created_by_user")
    updated_appointments = relationship("Appointment", foreign_keys="Appointment.updated_by_user_id", back_populates="updated_by_user")
    primary_doctor_appointments = relationship("Appointment", foreign_keys="Appointment.primary_doctor_id", back_populates="primary_doctor")
    created_patients = relationship("Patient", foreign_keys="[Patient.created_by_user_id]", back_populates="created_by_user")
    updated_patients = relationship("Patient", foreign_keys="[Patient.updated_by_user_id]", back_populates="updated_by_user")
    patient_user = relationship("Patient", foreign_keys="[Patient.user_id]", back_populates="user_account")
    created_resources = relationship("Resource", foreign_keys="[Resource.created_by_user_id]", back_populates="created_by_user")
    updated_resources = relationship("Resource", foreign_keys="[Resource.updated_by_user_id]", back_populates="updated_by_user")
    created_services = relationship("Service", foreign_keys="[Service.created_by_user_id]", back_populates="created_by_user")
    updated_services = relationship("Service", foreign_keys="[Service.updated_by_user_id]", back_populates="updated_by_user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
