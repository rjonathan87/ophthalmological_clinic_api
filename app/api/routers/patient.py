from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas import PatientCreate, PatientUpdate, PatientInDB, PatientResponse
from app.services.patient_service import PatientService
from app.api.dependencies import get_current_user, require_permission
from app.domain.schemas import UserInDB
from fastapi import status, HTTPException

router = APIRouter()

@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("patients.create"))
):
    service = PatientService(db)
    return service.create_patient(patient)

@router.get("/", response_model=List[PatientResponse])
def get_patients(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("patients.read"))
):
    service = PatientService(db)
    return service.get_patients(
        skip=skip,
        limit=limit,
        clinic_id=clinic_id,
        search=search
    )

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("patients.read"))
):
    service = PatientService(db)
    return service.get_patient(patient_id)

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("patients.update"))
):
    service = PatientService(db)
    return service.update_patient(patient_id, patient)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("patients.delete"))
):
    service = PatientService(db)
    if not service.delete_patient(patient_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return {"message": "Patient deleted successfully"}