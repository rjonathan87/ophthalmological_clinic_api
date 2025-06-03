from app.data.repositories.audit_log_repository import AuditLogRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class AuditLogService:
    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def create_audit_log(self, audit_log: schemas.AuditLogCreate) -> schemas.AuditLogInDB:
        return self.repository.create(audit_log)

    def get_audit_log(self, audit_log_id: int) -> Optional[schemas.AuditLogInDB]:
        return self.repository.get_by_id(audit_log_id)

    def get_audit_logs(self, skip: int = 0, limit: int = 100) -> List[schemas.AuditLogInDB]:
        return self.repository.get_all(skip, limit)

    def update_audit_log(self, audit_log_id: int, audit_log: schemas.AuditLogUpdate) -> Optional[schemas.AuditLogInDB]:
        return self.repository.update(audit_log_id, audit_log)

    def delete_audit_log(self, audit_log_id: int) -> bool:
        return self.repository.delete(audit_log_id)
