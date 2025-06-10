from pydantic import BaseModel, EmailStr, Field, HttpUrl, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal

from app.domain.models.performance_metrics_schemas import (
    PerformanceMetricCreate,
    PerformanceMetricUpdate,
    PerformanceMetricResponse,
    PerformanceMetricInDB,
    MetricCategoryEnum
)

# Schema para mensajes genéricos
class Message(BaseModel):
    message: str
    details: Optional[Dict[str, Any]] = None

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
    website: Optional[HttpUrl] = None
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
class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "PreferNotToSay"

class CommunicationChannelEnum(str, Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PHONE = "Phone"
    PORTAL = "Portal"

class PatientBase(BaseModel):
    clinic_id: int
    patient_identifier: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: Optional[GenderEnum]
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
    preferred_communication_channel: Optional[CommunicationChannelEnum]
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
class ResourceType(str, Enum):
    ROOM = "Room"
    EQUIPMENT = "Equipment"

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
    base_price: int = 0
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

class AppointmentUpdate(BaseModel):
    clinic_id: Optional[int] = None
    patient_id: Optional[int] = None
    primary_doctor_id: Optional[int] = None
    resource_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    appointment_type: Optional[str] = None
    status: Optional[str] = None
    reason_for_visit: Optional[str] = None
    cancellation_reason: Optional[str] = None
    confirmation_sent_at: Optional[datetime] = None
    reminder_sent_at: Optional[datetime] = None

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
    username: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

# Schemas para AppointmentServices (tabla de relación)
class AppointmentServiceBase(BaseModel):
    appointment_id: int
    service_id: int
    notes: Optional[str] = None

class AppointmentServiceCreate(AppointmentServiceBase):
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None

class AppointmentServiceInDB(AppointmentServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas para AuditLogs
class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    clinic_id: Optional[int] = None
    action_type: str = Field(..., description="Tipo de acción (CREATE, UPDATE, DELETE, LOGIN, etc.)")
    entity_type: str = Field(..., description="Tipo de entidad (Patient, Appointment, User, etc.)")
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
    review_notes: Optional[str] = None
    reviewed_by_user_id: Optional[int] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogUpdate(BaseModel):
    is_reviewed: Optional[bool] = None
    review_notes: Optional[str] = None
    reviewed_by_user_id: Optional[int] = None

class AuditLogInDB(AuditLogBase):
    id: int
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    user: Optional[UserInDB] = None
    clinic: Optional[ClinicInDB] = None
    reviewed_by_user: Optional[UserInDB] = None

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

# Schemas para Permissions
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDB(PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para EducationalResources
class EducationalResourceBase(BaseModel):
    title: str
    content_type: str
    content_url: str
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    language: Optional[str] = None

class EducationalResourceCreate(EducationalResourceBase):
    pass

class EducationalResourceUpdate(EducationalResourceBase):
    pass

class EducationalResourceInDB(EducationalResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para RolePermissions (tabla de relación entre roles y permisos)
class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionUpdate(RolePermissionBase):
    pass

class RolePermissionInDB(RolePermissionBase):
    class Config:
        from_attributes = True

# Schemas para Patient Education Tracking
class PatientEducationTrackingBase(BaseModel):
    patient_id: int
    resource_id: int
    status: str = Field('Assigned', pattern="^(Assigned|InProgress|Completed)$")
    progress: Optional[int] = 0
    feedback: Optional[str] = None
    quiz_results: Optional[dict] = None
    notes: Optional[str] = None
    completion_date: Optional[datetime] = None

class PatientEducationTrackingCreate(PatientEducationTrackingBase):
    pass

class PatientEducationTrackingUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(Assigned|InProgress|Completed)$")
    progress: Optional[int] = None
    feedback: Optional[str] = None
    quiz_results: Optional[dict] = None
    notes: Optional[str] = None
    completion_date: Optional[datetime] = None

class PatientEducationTrackingInDB(PatientEducationTrackingBase):
    id: int
    assigned_date: datetime
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PatientEducationTrackingResponse(PatientEducationTrackingInDB):
    patient: Optional[PatientInDB] = None
    resource: Optional[EducationalResourceInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para Consultations
class ConsultationBase(BaseModel):
    appointment_id: int
    patient_id: int
    clinic_id: int
    doctor_id: int
    consultation_date: datetime
    chief_complaint: str
    notes: Optional[str] = None
    consultation_type: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    consultation_status: str = Field('Completed', pattern="^(InProgress|Completed|Cancelled)$")

class ConsultationCreate(ConsultationBase):
    pass

class ConsultationUpdate(BaseModel):
    chief_complaint: Optional[str] = None
    notes: Optional[str] = None
    consultation_type: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    consultation_status: Optional[str] = Field(None, pattern="^(InProgress|Completed|Cancelled)$")

class ConsultationInDB(ConsultationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConsultationResponse(ConsultationInDB):
    appointment: Optional[AppointmentInDB] = None
    patient: Optional[PatientInDB] = None
    clinic: Optional[ClinicInDB] = None
    doctor: Optional[UserInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para Prescriptions
class PrescriptionBase(BaseModel):
    consultation_id: int
    patient_id: int
    prescribed_by_id: int
    prescription_type: str = Field(..., pattern="^(Medication|Optical|Contact Lens)$")
    prescription_details: dict
    instructions: Optional[str] = None
    expiration_date: Optional[datetime] = None
    is_active: bool = True

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    prescription_details: Optional[dict] = None
    instructions: Optional[str] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class PrescriptionInDB(PrescriptionBase):
    id: int
    prescription_date: datetime
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PrescriptionResponse(PrescriptionInDB):
    consultation: Optional[ConsultationInDB] = None
    patient: Optional[PatientInDB] = None
    prescribed_by: Optional[UserInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para RefractionExam
class RefractionExamBase(BaseModel):
    consultation_id: int
    exam_date: Optional[datetime] = None
    sphere_od: Optional[float] = None
    cylinder_od: Optional[float] = None
    axis_od: Optional[int] = None
    va_od: Optional[str] = None
    sphere_os: Optional[float] = None
    cylinder_os: Optional[float] = None
    axis_os: Optional[int] = None
    va_os: Optional[str] = None
    addition: Optional[float] = None
    ipd: Optional[float] = None
    notes: Optional[str] = None
    exam_data: Optional[dict] = None

class RefractionExamCreate(RefractionExamBase):
    pass

class RefractionExamUpdate(BaseModel):
    exam_date: Optional[datetime] = None
    sphere_od: Optional[float] = None
    cylinder_od: Optional[float] = None
    axis_od: Optional[int] = None
    va_od: Optional[str] = None
    sphere_os: Optional[float] = None
    cylinder_os: Optional[float] = None
    axis_os: Optional[int] = None
    va_os: Optional[str] = None
    addition: Optional[float] = None
    ipd: Optional[float] = None
    notes: Optional[str] = None
    exam_data: Optional[dict] = None

class RefractionExamInDB(RefractionExamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RefractionExamResponse(RefractionExamInDB):
    consultation: Optional[ConsultationInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para VisualAcuityExam
class VisualAcuityExamBase(BaseModel):
    consultation_id: int
    exam_date: Optional[datetime] = None
    uncorrected_va_od: Optional[str] = None
    uncorrected_va_os: Optional[str] = None
    current_correction_va_od: Optional[str] = None
    current_correction_va_os: Optional[str] = None
    new_correction_va_od: Optional[str] = None
    new_correction_va_os: Optional[str] = None
    test_method: Optional[str] = None
    test_distance: Optional[float] = None
    lighting_conditions: Optional[str] = None
    notes: Optional[str] = None
    exam_data: Optional[dict] = None

class VisualAcuityExamCreate(VisualAcuityExamBase):
    pass

class VisualAcuityExamUpdate(BaseModel):
    exam_date: Optional[datetime] = None
    uncorrected_va_od: Optional[str] = None
    uncorrected_va_os: Optional[str] = None
    current_correction_va_od: Optional[str] = None
    current_correction_va_os: Optional[str] = None
    new_correction_va_od: Optional[str] = None
    new_correction_va_os: Optional[str] = None
    test_method: Optional[str] = None
    test_distance: Optional[float] = None
    lighting_conditions: Optional[str] = None
    notes: Optional[str] = None
    exam_data: Optional[dict] = None

class VisualAcuityExamInDB(VisualAcuityExamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class VisualAcuityExamResponse(VisualAcuityExamInDB):
    consultation: Optional[ConsultationInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para IOPExam
class IOPExamBase(BaseModel):
    consultation_id: int
    exam_date: Optional[datetime] = None
    pressure_od: Optional[float] = None
    pressure_os: Optional[float] = None
    measurement_method: Optional[str] = None
    time_of_day: Optional[str] = None
    medication_used: Optional[str] = None
    notes: Optional[str] = None
    exam_data: Optional[dict] = None

class IOPExamCreate(IOPExamBase):
    pass

class IOPExamUpdate(BaseModel):
    exam_date: Optional[datetime] = None
    pressure_od: Optional[float] = None
    pressure_os: Optional[float] = None
    measurement_method: Optional[str] = None
    time_of_day: Optional[str] = None
    medication_used: Optional[str] = None
    notes: Optional[str] = None
    exam_data: Optional[dict] = None

class IOPExamInDB(IOPExamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IOPExamResponse(IOPExamInDB):
    consultation: Optional[ConsultationInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para PatientDocuments
class PatientDocumentBase(BaseModel):
    patient_id: int
    clinic_id: int
    document_type: str
    title: str
    file_path: str
    mime_type: str
    file_size: int
    document_date: datetime    
    description: Optional[str] = None
    status: str = Field('Active', pattern="^(Active|Archived|Deleted)$")
    is_private: bool = False
    document_metadata: Optional[dict] = None

class PatientDocumentCreate(PatientDocumentBase):
    pass

class PatientDocumentUpdate(BaseModel):
    title: Optional[str] = None
    document_type: Optional[str] = None    
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(Active|Archived|Deleted)$")
    is_private: Optional[bool] = None
    document_metadata: Optional[dict] = None

class PatientDocumentInDB(PatientDocumentBase):
    id: int
    upload_date: datetime
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PatientDocumentResponse(PatientDocumentInDB):
    patient: Optional[PatientInDB] = None
    clinic: Optional[ClinicInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para ConsentForms
class ConsentFormBase(BaseModel):
    patient_id: int
    clinic_id: int
    consultation_id: int
    appointment_id: int
    form_type: str
    title: str
    content: str
    signature_data: Optional[dict] = None
    signed_date: Optional[datetime] = None
    status: str = Field('Pending', pattern="^(Pending|Signed|Rejected|Expired)$")
    is_active: bool = True
    version: str
    signed_by_user_id: Optional[int] = None

class ConsentFormCreate(ConsentFormBase):
    pass

class ConsentFormUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    signature_data: Optional[dict] = None
    signed_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(Pending|Signed|Rejected|Expired)$")
    is_active: Optional[bool] = None
    signed_by_user_id: Optional[int] = None

class ConsentFormInDB(ConsentFormBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConsentFormResponse(ConsentFormInDB):
    patient: Optional[PatientInDB] = None
    clinic: Optional[ClinicInDB] = None
    consultation: Optional[ConsultationInDB] = None
    appointment: Optional[AppointmentInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None
    signed_by_user: Optional[UserInDB] = None

# Schemas para Facturas
class InvoiceBase(BaseModel):
    patient_id: int
    clinic_id: int
    consultation_id: Optional[int] = None
    appointment_id: Optional[int] = None
    invoice_number: str
    issue_date: datetime = Field(default_factory=datetime.now)
    due_date: datetime
    subtotal: float
    tax: float
    total: float
    payment_status: str = Field('Pending', pattern='^(Pending|Paid|Partially Paid|Overdue|Cancelled|Refunded)$')
    payment_method: Optional[str] = None
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    payment_status: Optional[str] = Field(None, pattern='^(Pending|Paid|Partially Paid|Overdue|Cancelled|Refunded)$')
    payment_method: Optional[str] = None
    notes: Optional[str] = None

class InvoiceInDB(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InvoiceResponse(InvoiceInDB):
    patient: Optional[PatientInDB] = None
    clinic: Optional[ClinicInDB] = None
    consultation: Optional[ConsultationInDB] = None
    appointment: Optional[AppointmentInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para InvoiceItems
class InvoiceItemBase(BaseModel):
    invoice_id: int
    service_id: Optional[int] = None
    description: str
    quantity: int = 1
    unit_price: float
    discount: float = 0.00
    total: float

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemUpdate(BaseModel):
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None

class InvoiceItemInDB(InvoiceItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InvoiceItemResponse(InvoiceItemInDB):
    invoice: Optional[InvoiceInDB] = None
    service: Optional[ServiceInDB] = None

# Schemas para Pagos
class PaymentBase(BaseModel):
    invoice_id: int
    patient_id: int
    clinic_id: int
    amount: float
    payment_date: datetime = Field(default_factory=datetime.now)
    payment_method: str = Field(..., description="Método de pago (Cash, Credit Card, Bank Transfer, Insurance, etc.)")
    transaction_id: Optional[str] = None
    payment_status: str = Field('Processed', pattern='^(Processed|Failed|Refunded|Voided)$')
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    payment_status: Optional[str] = Field(None, pattern='^(Processed|Failed|Refunded|Voided)$')
    notes: Optional[str] = None

class PaymentInDB(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaymentResponse(PaymentInDB):
    invoice: Optional[InvoiceInDB] = None
    patient: Optional[PatientInDB] = None
    clinic: Optional[ClinicInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

# Schemas para Performance Metrics
class MetricCategoryEnum(str, Enum):
    CLINICAL = "Clinical"
    FINANCIAL = "Financial" 
    OPERATIONAL = "Operational"
    PATIENT_SATISFACTION = "Patient Satisfaction"

class PerformanceMetricBase(BaseModel):
    clinic_id: int
    metric_name: str
    metric_value: Decimal = Field(..., decimal_places=2)
    metric_target: Optional[Decimal] = Field(None, decimal_places=2)
    measurement_date: datetime
    metric_category: MetricCategoryEnum
    description: Optional[str] = None
    notes: Optional[str] = None

class PerformanceMetricCreate(PerformanceMetricBase):
    pass

class PerformanceMetricUpdate(BaseModel):
    metric_name: Optional[str] = None
    metric_value: Optional[Decimal] = Field(None, decimal_places=2)
    metric_target: Optional[Decimal] = Field(None, decimal_places=2)
    measurement_date: Optional[datetime] = None
    metric_category: Optional[MetricCategoryEnum] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class PerformanceMetricInDB(PerformanceMetricBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PerformanceMetricResponse(PerformanceMetricInDB):
    clinic: Optional[ClinicInDB] = None
    created_by_user: Optional[UserInDB] = None
    updated_by_user: Optional[UserInDB] = None

    class Config:
        from_attributes = True

# Schemas para la cancelación de citas
class AppointmentCancellation(BaseModel):
    """Esquema para la cancelación de una cita"""
    reason: Optional[str] = None

# Enums para Lead
class LeadChannelEnum(str, Enum):
    WEBCHAT = "webchat"
    WHATSAPP = "whatsapp"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    PHONE = "phone"
    EMAIL = "email"
    WEBSITE = "website"
    REFERRAL = "referral"
    
class LeadStatusEnum(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    SCHEDULED = "scheduled"
    LOST = "lost"

# Schemas para Lead
class LeadBase(BaseModel):
    first_name: str
    last_name: str
    mobile_phone: str
    email: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    service_id: Optional[int] = None
    channel: LeadChannelEnum
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    status: LeadStatusEnum = LeadStatusEnum.NEW

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_phone: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    service_id: Optional[int] = None
    channel: Optional[LeadChannelEnum] = None
    status: Optional[LeadStatusEnum] = None
    appointment_id: Optional[int] = None
    notes: Optional[str] = None

class LeadStatusUpdate(BaseModel):
    status: LeadStatusEnum

class LeadInDB(LeadBase):
    lead_id: int
    status: LeadStatusEnum
    appointment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LeadResponse(LeadInDB):
    service: Optional[ServiceInDB] = None

# Schema para horarios alternativos sugeridos
class AppointmentAlternative(BaseModel):
    """Esquema para representar un horario alternativo para una cita."""
    start_time: datetime
    end_time: datetime
    doctor_id: Optional[int] = None  # Si es diferente al doctor original
    doctor_name: Optional[str] = None  # Nombre del doctor si es diferente
    
# Schema para verificación de disponibilidad de horarios
class AppointmentAvailabilityResponse(BaseModel):
    """Esquema para la respuesta de disponibilidad de horarios."""
    is_available: bool
    message: str
    alternative_slots: Optional[List[AppointmentAlternative]] = None
