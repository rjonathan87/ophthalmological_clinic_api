from .auth import auth_router
from .users import users_router
from .appointments import router as appointments_router
from .clinic import router as clinic_router
from .appointment_service import router as appointment_service_router
from .audit_log import router as audit_log_router
from .clinical_protocol import router as clinical_protocol_router
from .clinical_study import router as clinical_study_router
from .roles import router as roles_router
from .permission import router as permission_router
from .educational_resources import router as educational_resources_router
from .role_permission import router as role_permission_router
from .resource import router as resource_router
from .patient import router as patient_router
from .service import router as service_router
from .consultations import router as consultation_router
from .prescriptions import router as prescriptions_router
from .refractionexam import router as refractionexam_router
from .visualacuityexam import router as visualacuityexam_router

# Exportar los routers para que main.py pueda importarlos fácilmente
__all__ = [
    "auth_router",
    "users_router",
    "appointments_router",
    "clinic_router",
    "appointment_service_router",
    "audit_log_router",
    "clinical_protocol_router",
    "clinical_study_router",
    "roles_router",
    "permission_router",
    "educational_resources_router",
    "role_permission_router",
    "resource_router",
    "patient_router",
    "service_router",
    "consultation_router",
    "prescriptions_router",
    "refractionexam_router",
    "visualacuityexam_router"
]
