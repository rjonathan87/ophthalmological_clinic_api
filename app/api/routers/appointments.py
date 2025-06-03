from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.appointment_service import AppointmentService
from app.api.dependencies import get_current_user, require_permission
from app.domain.models import User as DBUser # Alias to avoid conflict with schemas.UserInDB

router = APIRouter()

@router.post("/", response_model=schemas.AppointmentResponse, status_code=status.HTTP_201_CREATED, summary="Create a new appointment")
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_permission("cita.agendar"))
):
    """
    Creates a new appointment in the system.
    Requires 'cita.agendar' permission.
    """
    service = AppointmentService(db)
    # Set created_by_user_id from the current user
    appointment_data = appointment.dict()
    appointment_data["created_by_user_id"] = current_user.id
    
    db_appointment = service.create_appointment(schemas.AppointmentCreate(**appointment_data))
    return db_appointment

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse, summary="Get an appointment by ID")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """
    Retrieves a single appointment by its ID.
    Requires 'cita.ver_todas' or 'cita.ver_propias' permission.
    If 'cita.ver_propias' is used, the appointment must belong to the current user's patient.
    """
    service = AppointmentService(db)
    db_appointment = service.get_appointment(appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    # Permission check: 'cita.ver_todas' allows viewing any appointment
    # 'cita.ver_propias' allows viewing appointments related to the user's patient
    if "cita.ver_todas" not in current_user.role.permissions and \
       (db_appointment.patient.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this appointment"
        )
    
    return db_appointment

@router.get("/", response_model=List[schemas.AppointmentResponse], summary="Get all appointments or filter by patient/clinic/doctor")
def get_appointments(
    patient_id: Optional[int] = None,
    clinic_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """
    Retrieves a list of appointments.
    Allows filtering by patient_id, clinic_id, or doctor_id.
    Requires 'cita.ver_todas' or 'cita.ver_propias' permission.
    If 'cita.ver_propias' is used, filters are applied to ensure only relevant appointments are returned.
    """
    service = AppointmentService(db)
    
    # Check for 'cita.ver_todas' permission
    if "cita.ver_todas" in current_user.role.permissions:
        if patient_id:
            appointments = service.get_appointments_by_patient(patient_id, skip, limit)
        elif clinic_id:
            appointments = service.get_appointments_by_clinic(clinic_id, skip, limit)
        elif doctor_id:
            appointments = service.get_appointments_by_doctor(doctor_id, skip, limit)
        else:
            appointments = service.get_appointments(skip, limit)
    elif "cita.ver_propias" in current_user.role.permissions:
        # If user has 'cita.ver_propias', they can only see their own patient's appointments
        # or appointments where they are the primary doctor.
        # First, try to get the patient associated with the current user
        user_patient = db.query(DBUser).filter(DBUser.id == current_user.id).first().patient_user
        
        if user_patient:
            # If the current user is a patient, they can only see their own appointments
            if patient_id and patient_id != user_patient.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to view other patients' appointments."
                )
            appointments = service.get_appointments_by_patient(user_patient.id, skip, limit)
        elif current_user.role.name == "Doctor": # Assuming 'Doctor' role implies primary_doctor_id
            if doctor_id and doctor_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to view other doctors' appointments."
                )
            appointments = service.get_appointments_by_doctor(current_user.id, skip, limit)
        else:
            # For other roles with 'cita.ver_propias', they might not have direct patient/doctor association
            # This case might need more specific logic based on how 'propias' is defined for other roles.
            # For now, we'll return an empty list or raise an error if no specific filter applies.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view appointments without specific filters or 'cita.ver_todas' permission."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to retrieve appointments"
        )
    
    return appointments

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse, summary="Update an existing appointment")
def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_permission("cita.agendar")) # Assuming update also requires agendar
):
    """
    Updates an existing appointment by its ID.
    Requires 'cita.agendar' permission.
    """
    service = AppointmentService(db)
    # Set updated_by_user_id from the current user
    appointment_data = appointment.dict()
    appointment_data["updated_by_user_id"] = current_user.id

    db_appointment = service.update_appointment(appointment_id, schemas.AppointmentUpdate(**appointment_data))
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an appointment")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_permission("cita.cancelar")) # Assuming delete requires cancelar
):
    """
    Deletes an appointment by its ID (soft delete).
    Requires 'cita.cancelar' permission.
    """
    service = AppointmentService(db)
    if not service.delete_appointment(appointment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}
