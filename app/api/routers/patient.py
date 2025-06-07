from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas import PatientCreate, PatientUpdate, PatientInDB
from app.services.patient_service import PatientService
from app.api.dependencies import get_current_user, require_permission
from app.domain.schemas import UserInDB

router = APIRouter()

@router.post("/", response_model=PatientInDB)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("paciente.crear"))
):
    service = PatientService(db)
    return service.create_patient(patient, current_user.id)

@router.get("/{patient_id}", response_model=PatientInDB)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("paciente.ver_todos"))
):
    service = PatientService(db)
    return service.get_patient(patient_id)

@router.get("/clinic/{clinic_id}", response_model=List[PatientInDB])
def get_clinic_patients(
    clinic_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("paciente.ver_asignados"))
):
    service = PatientService(db)
    return service.get_clinic_patients(clinic_id, skip, limit)

@router.get("/search/{clinic_id}", response_model=List[PatientInDB])
def search_patients(
    clinic_id: int,
    search_term: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("paciente.ver_asignados"))
):
    service = PatientService(db)
    return service.search_patients(clinic_id, search_term)

@router.put("/{patient_id}", response_model=PatientInDB)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("paciente.editar"))
):
    service = PatientService(db)
    return service.update_patient(patient_id, patient, current_user.id)

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("paciente.eliminar"))
):
    service = PatientService(db)
    service.delete_patient(patient_id)
    return {"message": "Patient deleted successfully"}