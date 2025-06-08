from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import and_
from datetime import datetime
from app.domain.models.patient_education_tracking import PatientEducationTracking
from app.domain.schemas import PatientEducationTrackingCreate, PatientEducationTrackingUpdate

class PatientEducationTrackingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tracking: PatientEducationTrackingCreate, created_by_user_id: int) -> PatientEducationTracking:
        db_tracking = PatientEducationTracking(**tracking.model_dump())
        db_tracking.created_by_user_id = created_by_user_id
        self.db.add(db_tracking)
        self.db.commit()
        self.db.refresh(db_tracking)
        return db_tracking

    def get_by_id(self, tracking_id: int) -> Optional[PatientEducationTracking]:
        return self.db.query(PatientEducationTracking).filter(
            and_(
                PatientEducationTracking.id == tracking_id,
                PatientEducationTracking.deleted_at.is_(None)
            )
        ).first()

    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[PatientEducationTracking]:
        return self.db.query(PatientEducationTracking).filter(
            and_(
                PatientEducationTracking.patient_id == patient_id,
                PatientEducationTracking.deleted_at.is_(None)
            )
        ).offset(skip).limit(limit).all()

    def get_by_resource_id(self, resource_id: int, skip: int = 0, limit: int = 100) -> List[PatientEducationTracking]:
        return self.db.query(PatientEducationTracking).filter(
            and_(
                PatientEducationTracking.resource_id == resource_id,
                PatientEducationTracking.deleted_at.is_(None)
            )
        ).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PatientEducationTracking]:
        return self.db.query(PatientEducationTracking).filter(
            PatientEducationTracking.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def update(self, tracking_id: int, tracking: PatientEducationTrackingUpdate, updated_by_user_id: int) -> Optional[PatientEducationTracking]:
        db_tracking = self.get_by_id(tracking_id)
        if db_tracking:
            update_data = tracking.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_tracking, field, value)
            db_tracking.updated_by_user_id = updated_by_user_id
            db_tracking.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_tracking)
        return db_tracking

    def soft_delete(self, tracking_id: int) -> bool:
        db_tracking = self.get_by_id(tracking_id)
        if db_tracking:
            db_tracking.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False

    def hard_delete(self, tracking_id: int) -> bool:
        db_tracking = self.get_by_id(tracking_id)
        if db_tracking:
            self.db.delete(db_tracking)
            self.db.commit()
            return True
        return False
