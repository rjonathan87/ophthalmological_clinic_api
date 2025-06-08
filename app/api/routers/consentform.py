from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.consentform_service import ConsentFormService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ConsentFormResponse)
def create_consent_form(
    consent_form: schemas.ConsentFormCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.crear"))
):
    service = ConsentFormService(db)
    return service.create_consent_form(consent_form, current_user.id)

@router.get("/", response_model=List[schemas.ConsentFormResponse])
def get_consent_forms(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    patient_id: Optional[int] = Query(None),
    appointment_id: Optional[int] = Query(None),
    consultation_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.ver"))
):
    service = ConsentFormService(db)
    return service.get_consent_forms(
        skip=skip,
        limit=limit,
        clinic_id=clinic_id,
        patient_id=patient_id,
        appointment_id=appointment_id,
        consultation_id=consultation_id,
        status=status
    )

@router.get("/{consent_form_id}", response_model=schemas.ConsentFormResponse)
def get_consent_form(
    consent_form_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.ver"))
):
    service = ConsentFormService(db)
    return service.get_consent_form(consent_form_id)

@router.get("/patient/{patient_id}", response_model=List[schemas.ConsentFormResponse])
def get_patient_consent_forms(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.ver"))
):
    service = ConsentFormService(db)
    return service.get_patient_consent_forms(patient_id, skip, limit)

@router.get("/clinic/{clinic_id}", response_model=List[schemas.ConsentFormResponse])
def get_clinic_consent_forms(
    clinic_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.ver"))
):
    service = ConsentFormService(db)
    return service.get_clinic_consent_forms(clinic_id, skip, limit)

@router.put("/{consent_form_id}", response_model=schemas.ConsentFormResponse)
def update_consent_form(
    consent_form_id: int,
    consent_form: schemas.ConsentFormUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.editar"))
):
    service = ConsentFormService(db)
    return service.update_consent_form(consent_form_id, consent_form, current_user.id)

@router.delete("/{consent_form_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consent_form(
    consent_form_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consentform.eliminar"))
):
    service = ConsentFormService(db)
    if not service.delete_consent_form(consent_form_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consent form not found"
        )
