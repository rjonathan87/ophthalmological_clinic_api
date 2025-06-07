from fastapi import APIRouter, Depends, Query
from typing import List
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
    current_user: UserInDB = Depends(require_permission("prescripcion.crear"))
):
    service = PrescriptionService(db)
    return service.create_prescription(prescription, current_user.id)

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.ver"))
):
    service = PrescriptionService(db)
    return service.get_prescription(prescription_id)

@router.get("/", response_model=List[PrescriptionResponse])
def get_prescriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.ver_todos"))
):
    service = PrescriptionService(db)
    return service.get_prescriptions(skip, limit)

@router.get("/patient/{patient_id}", response_model=List[PrescriptionResponse])
def get_patient_prescriptions(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.ver_paciente"))
):
    service = PrescriptionService(db)
    return service.get_patient_prescriptions(patient_id, skip, limit)

@router.get("/patient/{patient_id}/active", response_model=List[PrescriptionResponse])
def get_active_patient_prescriptions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.ver_paciente"))
):
    service = PrescriptionService(db)
    return service.get_active_patient_prescriptions(patient_id)

@router.get("/consultation/{consultation_id}", response_model=List[PrescriptionResponse])
def get_consultation_prescriptions(
    consultation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.ver_consulta"))
):
    service = PrescriptionService(db)
    return service.get_consultation_prescriptions(consultation_id, skip, limit)

@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.actualizar"))
):
    service = PrescriptionService(db)
    return service.update_prescription(prescription_id, prescription, current_user.id)

@router.delete("/{prescription_id}")
def delete_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("prescripcion.eliminar"))
):
    service = PrescriptionService(db)
    return service.delete_prescription(prescription_id)
