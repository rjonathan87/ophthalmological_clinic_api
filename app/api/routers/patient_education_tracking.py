from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas import (
    PatientEducationTrackingCreate,
    PatientEducationTrackingUpdate,
    PatientEducationTrackingResponse,
    UserInDB
)
from app.services.patient_education_tracking_service import PatientEducationTrackingService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter(
    tags=["Patient Education Tracking"]
)

@router.post("/", response_model=PatientEducationTrackingResponse)
def create_education_tracking(
    tracking: PatientEducationTrackingCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.crear"))
):
    service = PatientEducationTrackingService(db)
    return service.create_tracking(tracking, current_user.id)

@router.get("/{tracking_id}", response_model=PatientEducationTrackingResponse)
def get_education_tracking(
    tracking_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.ver"))
):
    service = PatientEducationTrackingService(db)
    return service.get_tracking(tracking_id)

@router.get("/patient/{patient_id}", response_model=List[PatientEducationTrackingResponse])
def get_patient_education_trackings(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.ver"))
):
    service = PatientEducationTrackingService(db)
    return service.get_patient_trackings(patient_id, skip, limit)

@router.get("/resource/{resource_id}", response_model=List[PatientEducationTrackingResponse])
def get_resource_education_trackings(
    resource_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.ver"))
):
    service = PatientEducationTrackingService(db)
    return service.get_resource_trackings(resource_id, skip, limit)

@router.get("/", response_model=List[PatientEducationTrackingResponse])
def get_all_education_trackings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.ver_todos"))
):
    service = PatientEducationTrackingService(db)
    return service.get_all_trackings(skip, limit)

@router.put("/{tracking_id}", response_model=PatientEducationTrackingResponse)
def update_education_tracking(
    tracking_id: int,
    tracking: PatientEducationTrackingUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.actualizar"))
):
    service = PatientEducationTrackingService(db)
    return service.update_tracking(tracking_id, tracking, current_user.id)

@router.delete("/{tracking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education_tracking(
    tracking_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("educacion.eliminar"))
):
    service = PatientEducationTrackingService(db)
    if not service.delete_tracking(tracking_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient education tracking not found"
        )
