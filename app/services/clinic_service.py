from fastapi import HTTPException
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
        clinic = self.repository.get_by_id(clinic_id)
        if not clinic:
            raise HTTPException(status_code=404, detail="Clínica no encontrada")
        return clinic

    def get_clinics(self, skip: int = 0, limit: int = 100) -> List[schemas.ClinicInDB]:
        return self.repository.get_all(skip, limit)

    def update_clinic(self, clinic_id: int, clinic: schemas.ClinicUpdate) -> schemas.ClinicInDB:
        updated_clinic = self.repository.update(clinic_id, clinic)
        if not updated_clinic:
            raise HTTPException(status_code=404, detail="Clínica no encontrada")
        return updated_clinic

    def delete_clinic(self, clinic_id: int) -> bool:
        if not self.repository.delete(clinic_id):
            raise HTTPException(status_code=404, detail="Clínica no encontrada")
        return True