from fastapi import HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.data.repositories.prescription_repository import PrescriptionRepository
from app.domain import schemas
from datetime import datetime

class PrescriptionService:
    def __init__(self, db: Session):
        self.repository = PrescriptionRepository(db)

    def create_prescription(self, prescription: schemas.PrescriptionCreate, created_by_user_id: int) -> schemas.PrescriptionInDB:
        return self.repository.create(prescription, created_by_user_id)

    def get_prescription(self, prescription_id: int) -> schemas.PrescriptionInDB:
        prescription = self.repository.get_by_id(prescription_id)
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
        return prescription

    def get_prescriptions(self, skip: int = 0, limit: int = 100) -> List[schemas.PrescriptionInDB]:
        return self.repository.get_all(skip, limit)

    def get_patient_prescriptions(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[schemas.PrescriptionInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)

    def get_consultation_prescriptions(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[schemas.PrescriptionInDB]:
        return self.repository.get_by_consultation_id(consultation_id, skip, limit)

    def get_active_patient_prescriptions(self, patient_id: int) -> List[schemas.PrescriptionInDB]:
        return self.repository.get_active_by_patient(patient_id)

    def update_prescription(self, prescription_id: int, prescription: schemas.PrescriptionUpdate, updated_by_user_id: int) -> schemas.PrescriptionInDB:
        updated_prescription = self.repository.update(prescription_id, prescription, updated_by_user_id)
        if not updated_prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
        return updated_prescription

    def delete_prescription(self, prescription_id: int) -> bool:
        if not self.repository.soft_delete(prescription_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
        return True
