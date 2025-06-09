from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionInDB,
    PrescriptionResponse,
    UserInDB
)
from app.services.prescription_service import PrescriptionService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=PrescriptionResponse)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.prescribe"))
):
    service = PrescriptionService(db)
    return service.create_prescription(prescription)

@router.get("/", response_model=List[PrescriptionResponse])
def get_prescriptions(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = Query(None),
    consultation_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.read"))
):
    service = PrescriptionService(db)
    return service.get_prescriptions(
        skip=skip,
        limit=limit,
        patient_id=patient_id,
        consultation_id=consultation_id
    )

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.read"))
):
    service = PrescriptionService(db)
    return service.get_prescription(prescription_id)

@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.prescribe"))
):
    service = PrescriptionService(db)
    return service.update_prescription(prescription_id, prescription)

@router.delete("/{prescription_id}", status_code=204)
def delete_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("consultations.prescribe"))
):
    service = PrescriptionService(db)
    if not service.delete_prescription(prescription_id):
        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )
    return {"message": "Prescription deleted successfully"}
