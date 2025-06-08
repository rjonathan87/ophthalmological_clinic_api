from fastapi import FastAPI
from app.api import routers
from app.api.routers import (
    refractionexam_router,
    visualacuityexam_router,
    iopexam_router,
    patientdocument_router,
    consentform_router,
    invoice_router,
    invoiceitem_router,
    payment_router,
    patient_education_tracking_router,
    performance_metrics_router
)

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    # Configuración de Swagger UI
    swagger_ui_parameters={
        "docExpansion": "none",  # Todas las secciones empiezan cerradas
        "defaultModelsExpandDepth": -1,  # Oculta la sección de esquemas por defecto
        "operationsSorter": "alpha",  # Ordena las operaciones alfabéticamente
        "tagsSorter": "alpha",  # Ordena los tags alfabéticamente
        "defaultModelExpandDepth": 2,  # Profundidad de expansión para los modelos
        "showExtensions": True,  # Muestra extensiones x-*
    }
)

# Incluir los routers de la API
app.include_router(routers.auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(routers.users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routers.appointments_router, prefix="/api/v1/appointments", tags=["Appointments"])
app.include_router(routers.clinic_router, prefix="/api/v1/clinics", tags=["Clinics"])
app.include_router(routers.appointment_service_router, prefix="/api/v1/appointment-services", tags=["Appointment Services"])
app.include_router(routers.audit_log_router, prefix="/api/v1/audit-logs", tags=["Audit Logs"])
app.include_router(routers.clinical_protocol_router, prefix="/api/v1/clinical-protocols", tags=["Clinical Protocols"])
app.include_router(routers.clinical_study_router, prefix="/api/v1/clinical-studies", tags=["Clinical Studies"])
app.include_router(routers.roles_router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(routers.permission_router, prefix="/api/v1/permissions", tags=["Permissions"])
app.include_router(routers.educational_resources_router, prefix="/api/v1/educational-resources", tags=["Educational Resources"])
app.include_router(routers.role_permission_router, prefix="/api/v1/role-permissions", tags=["Role Permissions"])
app.include_router(routers.resource_router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(routers.patient_router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(routers.service_router, prefix="/api/v1/services", tags=["Services"])
app.include_router(
    routers.consultation_router,
    prefix="/api/v1/consultations",
    tags=["Consultations"]
)
app.include_router(
    routers.prescriptions_router,
    prefix="/api/v1/prescriptions",
    tags=["Prescriptions"]
)
app.include_router(
    refractionexam_router,
    prefix="/api/v1/refractionexams",
    tags=["RefractionExams"]
)
app.include_router(
    visualacuityexam_router,
    prefix="/api/v1/visual-acuity-exams",
    tags=["VisualAcuityExams"]
)
app.include_router(
    iopexam_router,
    prefix="/api/v1/iopexams",
    tags=["IOP Exams"]
)
app.include_router(
    routers.patientdocument_router,
    prefix="/api/v1/patient-documents",
    tags=["Patient Documents"]
)
app.include_router(
    routers.patient_education_tracking_router,
    prefix="/api/v1/patient-education-trackings",
    tags=["Patient Education Trackings"]
)
app.include_router(
    routers.consentform_router,
    prefix="/api/v1/consent-forms",
    tags=["Consent Forms"]
)
app.include_router(
    routers.invoice_router,
    prefix="/api/v1/invoices",
    tags=["Invoices"]
)
app.include_router(
    routers.invoiceitem_router,
    prefix="/api/v1/invoice-items",
    tags=["Invoice Items"]
)
app.include_router(
    routers.payment_router,
    prefix="/api/v1/payments",
    tags=["Payments"]
)
app.include_router(
    performance_metrics_router,
    prefix="/api/v1/performance-metrics",
    tags=["Performance Metrics"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ophthalmological Clinic API!"}
