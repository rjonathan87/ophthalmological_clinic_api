from app.data.repositories.consentform_repository import ConsentFormRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class ConsentFormService:
    def __init__(self, db: Session):
        self.repository = ConsentFormRepository(db)

    def create_consent_form(self, consent_form: schemas.ConsentFormCreate, current_user_id: int) -> schemas.ConsentFormInDB:
        return self.repository.create(consent_form, current_user_id)

    def get_consent_form(self, consent_form_id: int) -> schemas.ConsentFormInDB:
        db_consent_form = self.repository.get_by_id(consent_form_id)
        if not db_consent_form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consent form not found"
            )
        return db_consent_form

    def get_consent_forms(
        self,
        skip: int = 0,
        limit: int = 100,
        clinic_id: Optional[int] = None,
        patient_id: Optional[int] = None,
        appointment_id: Optional[int] = None,
        consultation_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[schemas.ConsentFormInDB]:
        return self.repository.get_all(
            skip=skip,
            limit=limit,
            clinic_id=clinic_id,
            patient_id=patient_id,
            appointment_id=appointment_id,
            consultation_id=consultation_id,
            status=status
        )

    def get_patient_consent_forms(
        self,
        patient_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[schemas.ConsentFormInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)

    def get_clinic_consent_forms(
        self,
        clinic_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[schemas.ConsentFormInDB]:
        return self.repository.get_by_clinic_id(clinic_id, skip, limit)

    def update_consent_form(
        self,
        consent_form_id: int,
        consent_form: schemas.ConsentFormUpdate,
        current_user_id: int
    ) -> schemas.ConsentFormInDB:
        db_consent_form = self.repository.update(consent_form_id, consent_form, current_user_id)
        if not db_consent_form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consent form not found"
            )
        return db_consent_form

    def delete_consent_form(self, consent_form_id: int) -> bool:
        return self.repository.soft_delete(consent_form_id)
