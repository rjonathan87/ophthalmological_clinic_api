from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.models.patient import Patient
from app.domain.schemas import PatientCreate, PatientUpdate
from datetime import datetime
from sqlalchemy import or_

class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, patient: PatientCreate, created_by_user_id: int) -> Patient:
        db_patient = Patient(**patient.dict(), created_by_user_id=created_by_user_id)
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.db.query(Patient).filter(
            Patient.id == patient_id,
            Patient.deleted_at.is_(None)
        ).first()

    def get_by_email(self, email: str) -> Optional[Patient]:
        return self.db.query(Patient).filter(
            Patient.email == email,
            Patient.deleted_at.is_(None)
        ).first()

    def get_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[Patient]:
        return self.db.query(Patient).filter(
            Patient.clinic_id == clinic_id,
            Patient.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def search(self, clinic_id: int, search_term: str) -> List[Patient]:
        return self.db.query(Patient).filter(
            Patient.clinic_id == clinic_id,
            Patient.deleted_at.is_(None),
            or_(
                Patient.first_name.ilike(f"%{search_term}%"),
                Patient.last_name.ilike(f"%{search_term}%"),
                Patient.email.ilike(f"%{search_term}%"),
                Patient.patient_identifier.ilike(f"%{search_term}%")
            )
        ).all()

    def update(self, patient_id: int, patient: PatientUpdate, updated_by_user_id: int) -> Optional[Patient]:
        db_patient = self.get_by_id(patient_id)
        if db_patient:
            update_data = patient.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_patient, key, value)
            self.db.commit()
            self.db.refresh(db_patient)
        return db_patient

    def soft_delete(self, patient_id: int) -> bool:
        db_patient = self.get_by_id(patient_id)
        if db_patient:
            db_patient.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False