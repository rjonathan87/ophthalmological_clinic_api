from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.domain import schemas
from app.services.audit_log_service import AuditLogService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter(
    prefix="/audit-logs",
    tags=["Auditoría"]
)

@router.post("/", response_model=schemas.AuditLogInDB, status_code=status.HTTP_201_CREATED)
def create_audit_log(
    audit_log: schemas.AuditLogCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Crea un nuevo registro de auditoría.
    Solo usuarios autenticados pueden crear registros.
    """
    service = AuditLogService(db)
    return service.create_audit_log(audit_log)

@router.get("/", response_model=List[schemas.AuditLogInDB])
def read_audit_logs(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = None,
    user_id: Optional[int] = None,
    severity: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    is_reviewed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.audit_logs"))
):
    """
    Obtiene registros de auditoría con diversos filtros.
    Solo administradores pueden ver registros.
    """
    service = AuditLogService(db)
    
    if clinic_id:
        return service.get_clinic_audit_logs(clinic_id, skip, limit)
    elif user_id:
        return service.get_user_audit_logs(user_id, skip, limit)
    elif severity:
        return service.get_by_severity(severity, skip, limit)
    elif is_reviewed is not None:
        return service.get_unreviewed_audit_logs(skip, limit)
    else:
        return service.get_audit_logs(skip, limit)

@router.get("/{audit_log_id}", response_model=schemas.AuditLogInDB)
def read_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.audit_logs"))
):
    """
    Obtiene un registro de auditoría específico.
    Solo administradores pueden ver registros.
    """
    service = AuditLogService(db)
    return service.get_audit_log(audit_log_id)

@router.get("/entity/{entity_type}/{entity_id}", response_model=List[schemas.AuditLogInDB])
def read_entity_audit_logs(
    entity_type: str,
    entity_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.audit_logs"))
):
    """
    Obtiene registros de auditoría para una entidad específica.
    Solo administradores pueden ver registros.
    """
    service = AuditLogService(db)
    return service.get_entity_audit_logs(entity_type, entity_id)

@router.put("/{audit_log_id}/review", response_model=schemas.AuditLogInDB)
def review_audit_log(
    audit_log_id: int,
    review: schemas.AuditLogUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.audit_logs"))
):
    """
    Marca un registro de auditoría como revisado.
    Solo administradores pueden revisar registros.
    """
    service = AuditLogService(db)
    return service.update_audit_log(
        audit_log_id,
        review,
        reviewed_by_user_id=current_user.id
    )
