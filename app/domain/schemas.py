from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Schemas para Roles
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleInDB(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para Clínicas
class ClinicBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    timezone: str = 'UTC'
    is_active: bool = True

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(ClinicBase):
    name: Optional[str] = None
    timezone: Optional[str] = None
    is_active: Optional[bool] = None

class ClinicInDB(ClinicBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas para Usuarios
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    role_id: int
    associated_clinic_id: Optional[int] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    full_name: Optional[str] = None # Propiedad calculada

    class Config:
        from_attributes = True

class UserResponse(UserInDB):
    role: Optional[RoleInDB] = None
    clinic: Optional[ClinicInDB] = None

# Schemas para Pacientes
class PatientBase(BaseModel):
    clinic_id: int
    patient_identifier: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other|PreferNotToSay)$")
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    primary_care_physician: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    medical_history_summary: Optional[str] = None
    allergies: Optional[str] = None
    preferred_communication_channel: Optional[str] = Field(None, pattern="^(Email|SMS|Phone|Portal)$")
    gdpr_consent: bool = False
    user_id: Optional[int] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientInDB(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None
    full_name: Optional[str] = None # Propiedad calculada

    class Config:
        from_attributes = True

class PatientResponse(PatientInDB):
    clinic: Optional[ClinicInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None
    user_account: Optional[UserInDB] = None

# Schemas para Recursos
class ResourceBase(BaseModel):
    clinic_id: int
    name: str
    resource_type: str = Field(..., pattern="^(Room|Equipment)$")
    location: Optional[str] = None
    is_schedulable: bool = True
    is_active: bool = True

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(ResourceBase):
    pass

class ResourceInDB(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResourceResponse(ResourceInDB):
    clinic: Optional[ClinicInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para Servicios
class ServiceBase(BaseModel):
    clinic_id: int
    name: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    base_price: float = 0.00
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceInDB(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ServiceResponse(ServiceInDB):
    clinic: Optional[ClinicInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para Citas (Appointments)
class AppointmentBase(BaseModel):
    clinic_id: int
    patient_id: int
    primary_doctor_id: Optional[int] = None
    resource_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    appointment_type: Optional[str] = None
    status: str = Field('Scheduled', pattern="^(Scheduled|Confirmed|CheckedIn|InProgress|Completed|Cancelled|NoShow)$")
    reason_for_visit: Optional[str] = None
    cancellation_reason: Optional[str] = None
    confirmation_sent_at: Optional[datetime] = None
    reminder_sent_at: Optional[datetime] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class AppointmentInDB(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AppointmentResponse(AppointmentInDB):
    clinic: Optional[ClinicInDB] = None
    patient: Optional[PatientInDB] = None
    primary_doctor: Optional[UserInDB] = None
    resource: Optional[ResourceInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role_id: Optional[int] = None
    permissions: List[str] = [] # Añadimos los permisos para la autorización

# Schemas para AppointmentServices (tabla de relación)
class AppointmentServiceBase(BaseModel):
    appointment_id: int
    service_id: int

class AppointmentServiceCreate(AppointmentServiceBase):
    pass

class AppointmentServiceInDB(AppointmentServiceBase):
    class Config:
        from_attributes = True

# Schemas para AuditLogs
class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    clinic_id: Optional[int] = None
    action_type: str
    entity_type: str
    entity_id: Optional[str] = None
    details: Optional[str] = None
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    severity: Optional[str] = Field(None, pattern="^(Low|Medium|High|Critical)$")
    related_records: Optional[dict] = None
    system_component: Optional[str] = None
    is_reviewed: Optional[bool] = False
    reviewed_by_user_id: Optional[int] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogUpdate(AuditLogBase):
    # Audit logs are typically immutable, but allowing update for 'is_reviewed' and 'reviewed_by_user_id'
    is_reviewed: Optional[bool] = None
    reviewed_by_user_id: Optional[int] = None
    # Prevent updating other fields
    user_id: Optional[int] = Field(None, exclude=True)
    clinic_id: Optional[int] = Field(None, exclude=True)
    action_type: Optional[str] = Field(None, exclude=True)
    entity_type: Optional[str] = Field(None, exclude=True)
    entity_id: Optional[str] = Field(None, exclude=True)
    details: Optional[str] = Field(None, exclude=True)
    old_values: Optional[dict] = Field(None, exclude=True)
    new_values: Optional[dict] = Field(None, exclude=True)
    ip_address: Optional[str] = Field(None, exclude=True)
    user_agent: Optional[str] = Field(None, exclude=True)
    severity: Optional[str] = Field(None, exclude=True)
    related_records: Optional[dict] = Field(None, exclude=True)
    system_component: Optional[str] = Field(None, exclude=True)


class AuditLogInDB(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Schemas para ClinicalProtocols
class ClinicalProtocolBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    protocol_content: dict
    version: str
    is_active: Optional[bool] = True

class ClinicalProtocolCreate(ClinicalProtocolBase):
    pass

class ClinicalProtocolUpdate(ClinicalProtocolBase):
    name: Optional[str] = None
    category: Optional[str] = None
    protocol_content: Optional[dict] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None

class ClinicalProtocolInDB(ClinicalProtocolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para ClinicalStudies
class ClinicalStudyBase(BaseModel):
    name: str
    description: Optional[str] = None
    study_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str = Field(..., pattern="^(Active|Completed|Suspended)$")
    protocol_id: Optional[int] = None
    clinic_id: int
    is_active: bool = True

class ClinicalStudyCreate(ClinicalStudyBase):
    pass

class ClinicalStudyUpdate(ClinicalStudyBase):
    name: Optional[str] = None
    study_type: Optional[str] = None
    start_date: Optional[datetime] = None
    status: Optional[str] = None
    clinic_id: Optional[int] = None
    is_active: Optional[bool] = None

class ClinicalStudyInDB(ClinicalStudyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
