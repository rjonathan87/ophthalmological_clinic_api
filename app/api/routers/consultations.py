from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.consultation_service import ConsultationService
from app.api.dependencies import get_current_user, require_permission
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.ConsultationResponse)
def create_consultation(
    consultation: schemas.ConsultationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.create"))
):
    service = ConsultationService(db)
    return service.create_consultation(consultation)

@router.get("/", response_model=List[schemas.ConsultationResponse])
def get_consultations(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    patient_id: Optional[int] = Query(None),
    doctor_id: Optional[int] = Query(None),
    appointment_id: Optional[int] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.read"))
):
    service = ConsultationService(db)
    return service.get_consultations(
        skip=skip,
        limit=limit,
        clinic_id=clinic_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        date_from=date_from,
        date_to=date_to
    )

@router.get("/{consultation_id}", response_model=schemas.ConsultationResponse)
def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.read"))
):
    service = ConsultationService(db)
    return service.get_consultation(consultation_id)

@router.put("/{consultation_id}", response_model=schemas.ConsultationResponse)
def update_consultation(
    consultation_id: int,
    consultation: schemas.ConsultationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.update"))
):
    service = ConsultationService(db)
    return service.update_consultation(consultation_id, consultation)

@router.delete("/{consultation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.delete"))
):
    service = ConsultationService(db)
    if not service.delete_consultation(consultation_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    return {"message": "Consultation deleted successfully"}
