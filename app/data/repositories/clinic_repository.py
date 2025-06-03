from sqlalchemy.orm import Session
from app.domain import models, schemas
from typing import List, Optional

class ClinicRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, clinic: schemas.ClinicCreate) -> models.Clinic:
        db_clinic = models.Clinic(**clinic.model_dump())
        self.db.add(db_clinic)
        self.db.commit()
        self.db.refresh(db_clinic)
        return db_clinic

    def get_by_id(self, clinic_id: int) -> Optional[models.Clinic]:
        return self.db.query(models.Clinic).filter(models.Clinic.id == clinic_id, models.Clinic.deleted_at.is_(None)).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Clinic]:
        return self.db.query(models.Clinic).filter(models.Clinic.deleted_at.is_(None)).offset(skip).limit(limit).all()

    def update(self, clinic_id: int, clinic: schemas.ClinicUpdate) -> Optional[models.Clinic]:
        db_clinic = self.get_by_id(clinic_id)
        if db_clinic:
            update_data = clinic.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_clinic, key, value)
            self.db.commit()
            self.db.refresh(db_clinic)
        return db_clinic

    def delete(self, clinic_id: int) -> bool:
        db_clinic = self.get_by_id(clinic_id)
        if db_clinic:
            # Soft delete
            db_clinic.deleted_at = func.now()
            self.db.commit()
            return True
        return False
