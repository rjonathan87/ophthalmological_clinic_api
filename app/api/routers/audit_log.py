from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.audit_log_service import AuditLogService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.AuditLogInDB, status_code=status.HTTP_201_CREATED)
def create_audit_log(
    audit_log: schemas.AuditLogCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Assuming any authenticated user action can be logged
):
    service = AuditLogService(db)
    return service.create_audit_log(audit_log)

@router.get("/", response_model=List[schemas.AuditLogInDB])
def read_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_audit_logs")) # Assuming only admins can view audit logs
):
    service = AuditLogService(db)
    return service.get_audit_logs(skip, limit)

@router.get("/{audit_log_id}", response_model=schemas.AuditLogInDB)
def read_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_audit_logs")) # Assuming only admins can view a specific audit log
):
    service = AuditLogService(db)
    db_audit_log = service.get_audit_log(audit_log_id)
    if db_audit_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit Log not found")
    return db_audit_log

@router.put("/{audit_log_id}", response_model=schemas.AuditLogInDB)
def update_audit_log(
    audit_log_id: int,
    audit_log: schemas.AuditLogUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_audit_logs")) # Assuming only admins can update audit logs
):
    service = AuditLogService(db)
    db_audit_log = service.update_audit_log(audit_log_id, audit_log)
    if db_audit_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit Log not found")
    return db_audit_log

@router.delete("/{audit_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_audit_logs")) # Assuming only admins can delete audit logs
):
    service = AuditLogService(db)
    success = service.delete_audit_log(audit_log_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit Log not found")
    return {"detail": "Audit Log deleted successfully"}
