from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.clinic_service import ClinicService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ClinicInDB, status_code=status.HTTP_201_CREATED)
def create_clinic(
    clinic: schemas.ClinicCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas"))
):
    service = ClinicService(db)
    return service.create_clinic(clinic)

@router.get("/", response_model=List[schemas.ClinicInDB])
def read_clinics(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas")) # Assuming only admins can list all clinics
):
    service = ClinicService(db)
    return service.get_clinics(skip, limit)

@router.get("/{clinic_id}", response_model=schemas.ClinicInDB)
def read_clinic(
    clinic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas")) # Assuming only admins can get a specific clinic
):
    service = ClinicService(db)
    db_clinic = service.get_clinic(clinic_id)
    if db_clinic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")
    return db_clinic

@router.put("/{clinic_id}", response_model=schemas.ClinicInDB)
def update_clinic(
    clinic_id: int,
    clinic: schemas.ClinicUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas"))
):
    service = ClinicService(db)
    db_clinic = service.update_clinic(clinic_id, clinic)
    if db_clinic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")
    return db_clinic

@router.delete("/{clinic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinic(
    clinic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas"))
):
    service = ClinicService(db)
    success = service.delete_clinic(clinic_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")
    return {"detail": "Clinic deleted successfully"}
