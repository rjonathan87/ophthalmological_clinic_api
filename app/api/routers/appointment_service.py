from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.appointment_service_service import AppointmentServiceService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.AppointmentServiceInDB, status_code=status.HTTP_201_CREATED)
def create_appointment_service(
    appointment_service: schemas.AppointmentServiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointment.manage_services"))
):
    service = AppointmentServiceService(db)
    return service.create_appointment_service(appointment_service, current_user.id)

@router.get("/{appointment_id}/services", response_model=List[schemas.AppointmentServiceInDB])
def get_services_for_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointment.manage_services"))
):
    service = AppointmentServiceService(db)
    return service.get_services_for_appointment(appointment_id)

@router.get("/service/{service_id}/appointments", response_model=List[schemas.AppointmentServiceInDB])
def get_appointments_for_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointment.manage_services"))
):
    service = AppointmentServiceService(db)
    return service.get_appointments_for_service(service_id)

@router.get("/{appointment_id}/{service_id}", response_model=schemas.AppointmentServiceInDB)
def get_appointment_service(
    appointment_id: int,
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointment.manage_services"))
):
    service = AppointmentServiceService(db)
    db_appointment_service = service.get_appointment_service(appointment_id, service_id)
    if db_appointment_service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment Service link not found")
    return db_appointment_service

@router.delete("/{appointment_id}/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment_service(
    appointment_id: int,
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointment.manage_services"))
):
    service = AppointmentServiceService(db)
    success = service.delete_appointment_service(appointment_id, service_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment Service link not found")
    return {"detail": "Appointment Service link deleted successfully"}
