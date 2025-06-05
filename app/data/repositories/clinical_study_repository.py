from sqlalchemy.orm import Session
from app.domain import schemas
from typing import List, Optional

from app.domain.models import ClinicalStudy

class ClinicalStudyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, study: schemas.ClinicalStudyCreate) -> ClinicalStudy:
        db_study = ClinicalStudy(**study.model_dump())
        self.db.add(db_study)
        self.db.commit()
        self.db.refresh(db_study)
        return db_study

    def get_by_id(self, study_id: int) -> Optional[ClinicalStudy]:
        return self.db.query(ClinicalStudy).filter(ClinicalStudy.id == study_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ClinicalStudy]:
        return self.db.query(ClinicalStudy).offset(skip).limit(limit).all()

    def update(self, study_id: int, study: schemas.ClinicalStudyUpdate) -> Optional[ClinicalStudy]:
        db_study = self.get_by_id(study_id)
        if db_study:
            update_data = study.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_study, key, value)
            self.db.commit()
            self.db.refresh(db_study)
        return db_study

    def delete(self, study_id: int) -> bool:
        db_study = self.get_by_id(study_id)
        if db_study:
            self.db.delete(db_study)
            self.db.commit()
            return True
        return False
