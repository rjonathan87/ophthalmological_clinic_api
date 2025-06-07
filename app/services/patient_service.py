from typing import List, Optional
from sqlalchemy.orm import Session
from app.data.repositories.patient_repository import PatientRepository
from app.domain.schemas import PatientCreate, PatientUpdate, PatientInDB
from fastapi import HTTPException

class PatientService:
    def __init__(self, db: Session):
        self.repository = PatientRepository(db)

    def create_patient(self, patient: PatientCreate, created_by_user_id: int) -> PatientInDB:
        # Verificar si ya existe un paciente con el mismo email
        if patient.email:
            existing_patient = self.repository.get_by_email(patient.email)
            if existing_patient:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        return self.repository.create(patient, created_by_user_id)

    def get_patient(self, patient_id: int) -> Optional[PatientInDB]:
        patient = self.repository.get_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    def get_clinic_patients(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PatientInDB]:
        return self.repository.get_by_clinic(clinic_id, skip, limit)

    def search_patients(self, clinic_id: int, search_term: str) -> List[PatientInDB]:
        return self.repository.search(clinic_id, search_term)

    def update_patient(self, patient_id: int, patient: PatientUpdate, updated_by_user_id: int) -> PatientInDB:
        updated_patient = self.repository.update(patient_id, patient, updated_by_user_id)
        if not updated_patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return updated_patient

    def delete_patient(self, patient_id: int) -> bool:
        success = self.repository.soft_delete(patient_id)
        if not success:
            raise HTTPException(status_code=404, detail="Patient not found")
        return True