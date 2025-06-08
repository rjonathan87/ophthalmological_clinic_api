from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional
from datetime import datetime

from app.domain.models.auditlog import AuditLog
from app.domain import schemas

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
        return self.db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog)\
            .filter(AuditLog.clinic_id == clinic_id)\
            .order_by(AuditLog.created_at.desc())\
            .offset(skip).limit(limit).all()

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog)\
            .filter(AuditLog.user_id == user_id)\
            .order_by(AuditLog.created_at.desc())\
            .offset(skip).limit(limit).all()

    def get_by_entity(self, entity_type: str, entity_id: str) -> List[AuditLog]:
        return self.db.query(AuditLog)\
            .filter(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id
            )\
            .order_by(AuditLog.created_at.desc())\
            .all()

    def get_unreviewed(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog)\
            .filter(AuditLog.is_reviewed == False)\
            .order_by(AuditLog.created_at.desc())\
            .offset(skip).limit(limit).all()

    def update(self, audit_log_id: int, audit_log: schemas.AuditLogUpdate, reviewed_by_user_id: Optional[int] = None) -> Optional[AuditLog]:
        db_audit_log = self.get_by_id(audit_log_id)
        if db_audit_log:
            update_data = audit_log.model_dump(exclude_unset=True)
            
            # Si se está marcando como revisado, actualizar campos relacionados
            if update_data.get('is_reviewed') == True:
                update_data['reviewed_at'] = datetime.now()
                if reviewed_by_user_id:
                    update_data['reviewed_by_user_id'] = reviewed_by_user_id

            for key, value in update_data.items():
                setattr(db_audit_log, key, value)
            
            self.db.commit()
            self.db.refresh(db_audit_log)
            return db_audit_log
        return None

    def get_by_severity(self, severity: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog)\
            .filter(AuditLog.severity == severity)\
            .order_by(AuditLog.created_at.desc())\
            .offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog)\
            .filter(
                AuditLog.created_at >= start_date,
                AuditLog.created_at <= end_date
            )\
            .order_by(AuditLog.created_at.desc())\
            .offset(skip).limit(limit).all()
