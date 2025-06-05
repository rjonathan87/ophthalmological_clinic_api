from sqlalchemy.orm import Session
from app.domain import schemas
from typing import List, Optional

from app.domain.models import AuditLog

class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, audit_log: schemas.AuditLogCreate) -> AuditLog:
        db_audit_log = AuditLog(**audit_log.model_dump())
        self.db.add(db_audit_log)
        self.db.commit()
        self.db.refresh(db_audit_log)
        return db_audit_log

    def get_by_id(self, audit_log_id: int) -> Optional[AuditLog]:
        return self.db.query(AuditLog).filter(AuditLog.id == audit_log_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).offset(skip).limit(limit).all()

    def update(self, audit_log_id: int, audit_log: schemas.AuditLogUpdate) -> Optional[AuditLog]:
        db_audit_log = self.get_by_id(audit_log_id)
        if db_audit_log:
            update_data = audit_log.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_audit_log, key, value)
            self.db.commit()
            self.db.refresh(db_audit_log)
        return db_audit_log

    def delete(self, audit_log_id: int) -> bool:
        db_audit_log = self.get_by_id(audit_log_id)
        if db_audit_log:
            self.db.delete(db_audit_log)
            self.db.commit()
            return True
        return False
