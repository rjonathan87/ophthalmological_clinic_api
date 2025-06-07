from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.consultation_service import ConsultationService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ConsultationResponse)
def create_consultation(
    consultation: schemas.ConsultationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consulta.crear"))
):
    service = ConsultationService(db)
    return service.create_consultation(consultation, current_user.id)

@router.get("/", response_model=List[schemas.ConsultationResponse])
def get_consultations(
    patient_id: Optional[int] = None,
    clinic_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consulta.ver"))
):
    service = ConsultationService(db)
    
    if patient_id:
        return service.get_consultations_by_patient(patient_id, skip, limit)
    elif clinic_id:
        return service.get_consultations_by_clinic(clinic_id, skip, limit)
    elif doctor_id:
        return service.get_consultations_by_doctor(doctor_id, skip, limit)
    return service.get_consultations(skip, limit)

@router.get("/{consultation_id}", response_model=schemas.ConsultationResponse)
def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consulta.ver"))
):
    service = ConsultationService(db)
    return service.get_consultation(consultation_id)

@router.put("/{consultation_id}", response_model=schemas.ConsultationResponse)
def update_consultation(
    consultation_id: int,
    consultation: schemas.ConsultationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consulta.editar"))
):
    service = ConsultationService(db)
    return service.update_consultation(consultation_id, consultation, current_user.id)

@router.delete("/{consultation_id}")
def delete_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consulta.eliminar"))
):
    service = ConsultationService(db)
    return service.delete_consultation(consultation_id)
