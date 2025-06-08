from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from sqlalchemy import or_
from app.domain.models.consentform import ConsentForm
from app.domain.schemas import ConsentFormCreate, ConsentFormUpdate

class ConsentFormRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, consent_form: ConsentFormCreate, created_by_user_id: int) -> ConsentForm:
        db_consent_form = ConsentForm(
            **consent_form.dict(),
            created_by_user_id=created_by_user_id
        )
        self.db.add(db_consent_form)
        self.db.commit()
        self.db.refresh(db_consent_form)
        return db_consent_form

    def get_by_id(self, consent_form_id: int) -> Optional[ConsentForm]:
        return self.db.query(ConsentForm).filter(
            ConsentForm.id == consent_form_id,
            ConsentForm.deleted_at.is_(None)
        ).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        clinic_id: Optional[int] = None,
        patient_id: Optional[int] = None,
        appointment_id: Optional[int] = None,
        consultation_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[ConsentForm]:
        query = self.db.query(ConsentForm).filter(ConsentForm.deleted_at.is_(None))

        if clinic_id:
            query = query.filter(ConsentForm.clinic_id == clinic_id)
        if patient_id:
            query = query.filter(ConsentForm.patient_id == patient_id)
        if appointment_id:
            query = query.filter(ConsentForm.appointment_id == appointment_id)
        if consultation_id:
            query = query.filter(ConsentForm.consultation_id == consultation_id)
        if status:
            query = query.filter(ConsentForm.status == status)

        return query.offset(skip).limit(limit).all()

    def get_by_patient_id(
        self,
        patient_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ConsentForm]:
        return self.db.query(ConsentForm).filter(
            ConsentForm.patient_id == patient_id,
            ConsentForm.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def get_by_clinic_id(
        self,
        clinic_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ConsentForm]:
        return self.db.query(ConsentForm).filter(
            ConsentForm.clinic_id == clinic_id,
            ConsentForm.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def update(
        self,
        consent_form_id: int,
        consent_form: ConsentFormUpdate,
        updated_by_user_id: int
    ) -> Optional[ConsentForm]:
        db_consent_form = self.get_by_id(consent_form_id)
        if db_consent_form:
            update_data = consent_form.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for field, value in update_data.items():
                setattr(db_consent_form, field, value)
            self.db.commit()
            self.db.refresh(db_consent_form)
        return db_consent_form

    def soft_delete(self, consent_form_id: int) -> bool:
        db_consent_form = self.get_by_id(consent_form_id)
        if db_consent_form:
            db_consent_form.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
