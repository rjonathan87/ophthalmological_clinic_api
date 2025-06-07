from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.domain.models.prescription import Prescription
from app.domain.schemas import PrescriptionCreate, PrescriptionUpdate
from datetime import datetime

class PrescriptionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, prescription: PrescriptionCreate, created_by_user_id: int) -> Prescription:
        db_prescription = Prescription(
            **prescription.dict(),
            created_by_user_id=created_by_user_id,
            updated_by_user_id=created_by_user_id
        )
        self.db.add(db_prescription)
        self.db.commit()
        self.db.refresh(db_prescription)
        return db_prescription

    def get_by_id(self, prescription_id: int) -> Optional[Prescription]:
        return self.db.query(Prescription).filter(
            Prescription.id == prescription_id,
            Prescription.deleted_at.is_(None)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Prescription]:
        return self.db.query(Prescription).filter(
            Prescription.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[Prescription]:
        return self.db.query(Prescription).filter(
            Prescription.patient_id == patient_id,
            Prescription.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def get_by_consultation_id(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[Prescription]:
        return self.db.query(Prescription).filter(
            Prescription.consultation_id == consultation_id,
            Prescription.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def get_active_by_patient(self, patient_id: int) -> List[Prescription]:
        return self.db.query(Prescription).filter(
            Prescription.patient_id == patient_id,
            Prescription.is_active == True,
            Prescription.deleted_at.is_(None),
            Prescription.expiration_date > datetime.utcnow()
        ).all()

    def update(self, prescription_id: int, prescription: PrescriptionUpdate, updated_by_user_id: int) -> Optional[Prescription]:
        db_prescription = self.get_by_id(prescription_id)
        if db_prescription:
            update_data = prescription.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_prescription, key, value)
            self.db.commit()
            self.db.refresh(db_prescription)
        return db_prescription

    def soft_delete(self, prescription_id: int) -> bool:
        db_prescription = self.get_by_id(prescription_id)
        if db_prescription:
            db_prescription.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
