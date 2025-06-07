from app.data.repositories.consultation_repository import ConsultationRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class ConsultationService:
    def __init__(self, db: Session):
        self.repository = ConsultationRepository(db)

    def create_consultation(self, consultation: schemas.ConsultationCreate, created_by_user_id: int) -> schemas.ConsultationInDB:
        return self.repository.create(consultation, created_by_user_id)

    def get_consultation(self, consultation_id: int) -> Optional[schemas.ConsultationInDB]:
        consultation = self.repository.get_by_id(consultation_id)
        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )
        return consultation

    def get_consultations(self, skip: int = 0, limit: int = 100) -> List[schemas.ConsultationInDB]:
        return self.repository.get_all(skip, limit)

    def get_consultations_by_patient(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[schemas.ConsultationInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)

    def get_consultations_by_doctor(self, doctor_id: int, skip: int = 0, limit: int = 100) -> List[schemas.ConsultationInDB]:
        return self.repository.get_by_doctor_id(doctor_id, skip, limit)

    def get_consultations_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[schemas.ConsultationInDB]:
        return self.repository.get_by_clinic_id(clinic_id, skip, limit)

    def update_consultation(self, consultation_id: int, consultation: schemas.ConsultationUpdate, updated_by_user_id: int) -> Optional[schemas.ConsultationInDB]:
        updated_consultation = self.repository.update(consultation_id, consultation, updated_by_user_id)
        if not updated_consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )
        return updated_consultation

    def delete_consultation(self, consultation_id: int) -> bool:
        if not self.repository.soft_delete(consultation_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )
        return True
