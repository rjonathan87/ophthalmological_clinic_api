from app.data.repositories.clinical_study_repository import ClinicalStudyRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class ClinicalStudyService:
    def __init__(self, db: Session):
        self.repository = ClinicalStudyRepository(db)

    def create_study(self, study: schemas.ClinicalStudyCreate) -> schemas.ClinicalStudyInDB:
        return self.repository.create(study)

    def get_study(self, study_id: int) -> Optional[schemas.ClinicalStudyInDB]:
        return self.repository.get_by_id(study_id)

    def get_studies(self, skip: int = 0, limit: int = 100) -> List[schemas.ClinicalStudyInDB]:
        return self.repository.get_all(skip, limit)

    def update_study(self, study_id: int, study: schemas.ClinicalStudyUpdate) -> Optional[schemas.ClinicalStudyInDB]:
        return self.repository.update(study_id, study)

    def delete_study(self, study_id: int) -> bool:
        return self.repository.delete(study_id)
