from app.data.repositories.clinic_repository import ClinicRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class ClinicService:
    def __init__(self, db: Session):
        self.repository = ClinicRepository(db)

    def create_clinic(self, clinic: schemas.ClinicCreate) -> schemas.ClinicInDB:
        return self.repository.create(clinic)

    def get_clinic(self, clinic_id: int) -> Optional[schemas.ClinicInDB]:
        return self.repository.get_by_id(clinic_id)

    def get_clinics(self, skip: int = 0, limit: int = 100) -> List[schemas.ClinicInDB]:
        return self.repository.get_all(skip, limit)

    def update_clinic(self, clinic_id: int, clinic: schemas.ClinicUpdate) -> Optional[schemas.ClinicInDB]:
        return self.repository.update(clinic_id, clinic)

    def delete_clinic(self, clinic_id: int) -> bool:
        return self.repository.delete(clinic_id)
