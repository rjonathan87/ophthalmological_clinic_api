from sqlalchemy.orm import Session
from app.domain import schemas
from typing import List, Optional
from datetime import datetime

from app.domain.models.consultation import Consultation

class ConsultationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, consultation: schemas.ConsultationCreate, created_by_user_id: int) -> Consultation:
        db_consultation = Consultation(
            **consultation.dict(),
            created_by_user_id=created_by_user_id,
            updated_by_user_id=created_by_user_id
        )
        self.db.add(db_consultation)
        self.db.commit()
        self.db.refresh(db_consultation)
        return db_consultation

    def get_by_id(self, consultation_id: int) -> Optional[Consultation]:
        return self.db.query(Consultation).filter(
            Consultation.id == consultation_id,
            Consultation.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Consultation]:
        return self.db.query(Consultation).filter(
            Consultation.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[Consultation]:
        return self.db.query(Consultation).filter(
            Consultation.patient_id == patient_id,
            Consultation.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_doctor_id(self, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Consultation]:
        return self.db.query(Consultation).filter(
            Consultation.doctor_id == doctor_id,
            Consultation.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_clinic_id(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[Consultation]:
        return self.db.query(Consultation).filter(
            Consultation.clinic_id == clinic_id,
            Consultation.deleted_at == None
        ).offset(skip).limit(limit).all()

    def update(self, consultation_id: int, consultation: schemas.ConsultationUpdate, updated_by_user_id: int) -> Optional[Consultation]:
        db_consultation = self.get_by_id(consultation_id)
        if db_consultation:
            update_data = consultation.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_consultation, key, value)
            self.db.commit()
            self.db.refresh(db_consultation)
        return db_consultation

    def soft_delete(self, consultation_id: int) -> bool:
        db_consultation = self.get_by_id(consultation_id)
        if db_consultation:
            db_consultation.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
