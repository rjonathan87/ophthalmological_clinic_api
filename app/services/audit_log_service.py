from app.data.repositories.audit_log_repository import AuditLogRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class AuditLogService:
    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def create_audit_log(self, audit_log: schemas.AuditLogCreate) -> schemas.AuditLogInDB:
        return self.repository.create(audit_log)

    def get_audit_log(self, audit_log_id: int) -> schemas.AuditLogInDB:
        db_audit_log = self.repository.get_by_id(audit_log_id)
        if not db_audit_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de auditoría no encontrado"
            )
        return db_audit_log

    def get_audit_logs(self, skip: int = 0, limit: int = 100) -> List[schemas.AuditLogInDB]:
        return self.repository.get_all(skip, limit)

    def get_clinic_audit_logs(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[schemas.AuditLogInDB]:
        return self.repository.get_by_clinic(clinic_id, skip, limit)

    def get_user_audit_logs(self, user_id: int, skip: int = 0, limit: int = 100) -> List[schemas.AuditLogInDB]:
        return self.repository.get_by_user(user_id, skip, limit)

    def get_entity_audit_logs(self, entity_type: str, entity_id: str) -> List[schemas.AuditLogInDB]:
        return self.repository.get_by_entity(entity_type, entity_id)

    def get_unreviewed_audit_logs(self, skip: int = 0, limit: int = 100) -> List[schemas.AuditLogInDB]:
        return self.repository.get_unreviewed(skip, limit)

    def update_audit_log(self, 
                        audit_log_id: int, 
                        audit_log: schemas.AuditLogUpdate,
                        reviewed_by_user_id: Optional[int] = None) -> Optional[schemas.AuditLogInDB]:
        updated_log = self.repository.update(audit_log_id, audit_log, reviewed_by_user_id)
        if not updated_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de auditoría no encontrado"
            )
        return updated_log

    def delete_audit_log(self, audit_log_id: int) -> bool:
        return self.repository.delete(audit_log_id)
