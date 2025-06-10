from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.appointment_service import AppointmentService
from app.api.dependencies import get_current_user, require_permission
from app.domain.models import User as DBUser # Alias to avoid conflict with schemas.UserInDB
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.create"))
):
    """
    Creates a new appointment in the system.
    Requires 'appointments.create' permission.
    """
    service = AppointmentService(db)
    # Set created_by_user_id from the current user
    appointment_data = appointment.dict()
    appointment_data["created_by_user_id"] = current_user.id
    
    db_appointment = service.create_appointment(schemas.AppointmentCreate(**appointment_data))
    return db_appointment

@router.get("/", response_model=List[schemas.AppointmentResponse])
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    patient_id: Optional[int] = Query(None),
    doctor_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Retrieves a list of appointments.
    Allows filtering by patient_id, clinic_id, or doctor_id.
    Requires 'appointments.read' permission.
    """
    service = AppointmentService(db)
    return service.get_appointments(
        skip=skip, 
        limit=limit,
        clinic_id=clinic_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
        status=status,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/check-availability", response_model=schemas.AppointmentAvailabilityResponse)
def check_time_slot_availability(
    clinic_id: int,
    doctor_id: int,
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    num_alternatives: Optional[int] = Query(3, description="Número de alternativas a sugerir"),
    days_range: Optional[int] = Query(7, description="Rango de días en el futuro para buscar alternativas"),
    check_other_doctors: Optional[bool] = Query(True, description="Si se deben verificar otros médicos como alternativa"),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Verifica la disponibilidad de un horario para agendar una cita.
    Si el horario no está disponible, sugiere horarios alternativos.
    
    Args:
        clinic_id: ID de la clínica
        doctor_id: ID del doctor
        resource_id: ID del recurso (consultorio)
        start_time: Hora de inicio propuesta
        end_time: Hora de fin propuesta
        num_alternatives: Número de alternativas a sugerir (por defecto 3)
        days_range: Rango de días en el futuro para buscar alternativas (por defecto 7)
        check_other_doctors: Si se deben verificar otros médicos como alternativa (por defecto True)
        
    Returns:
        Un objeto indicando si el horario está disponible y posibles alternativas
    
    Requires 'appointments.read' permission.
    """
    try:
        service = AppointmentService(db)
        is_available = service.is_time_slot_available(
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Si el horario está disponible, no necesitamos alternativas
        if is_available:
            return schemas.AppointmentAvailabilityResponse(
                is_available=True,
                message="El horario está disponible",
                alternative_slots=[]
            )
        
        # Si no está disponible, buscamos alternativas
        alternative_slots = service.find_alternative_slots(
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            num_alternatives=num_alternatives,
            days_range=days_range,
            check_other_doctors=check_other_doctors
        )
        
        message = "El horario no está disponible"
        if alternative_slots:
            message += ". Se han encontrado horarios alternativos."
        else:
            message += ". No se encontraron horarios alternativos en los próximos días."
        
        return schemas.AppointmentAvailabilityResponse(
            is_available=False,
            message=message,
            alternative_slots=alternative_slots
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar disponibilidad: {str(e)}"
        )

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Retrieves a single appointment by its ID.
    Requires 'appointments.read' permission.
    """
    service = AppointmentService(db)
    db_appointment = service.get_appointment(appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    return db_appointment

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.update"))
):
    """
    Updates an existing appointment by its ID.
    Requires 'appointments.update' permission.
    """
    service = AppointmentService(db)
    # Set updated_by_user_id from the current user
    appointment_data = appointment.dict()
    appointment_data["updated_by_user_id"] = current_user.id

    db_appointment = service.update_appointment(appointment_id, schemas.AppointmentUpdate(**appointment_data))
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.delete"))
):
    """
    Deletes an appointment by its ID (soft delete).
    Requires 'appointments.delete' permission.
    """
    service = AppointmentService(db)
    if not service.delete_appointment(appointment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

@router.post("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    cancellation_data: Optional[schemas.AppointmentCancellation] = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.cancel"))
):
    """
    Cancels an appointment by its ID.
    Optionally accepts a reason for cancellation.
    Requires 'appointments.cancel' permission.
    """
    service = AppointmentService(db)
    cancellation_reason = cancellation_data.reason if cancellation_data is not None else None
    if not service.cancel_appointment(appointment_id, cancellation_reason):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"message": "Appointment canceled successfully"}

@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.create"))
):
    """
    Creates a new appointment in the system.
    Requires 'appointments.create' permission.
    """
    service = AppointmentService(db)
    # Set created_by_user_id from the current user
    appointment_data = appointment.dict()
    appointment_data["created_by_user_id"] = current_user.id
    
    db_appointment = service.create_appointment(schemas.AppointmentCreate(**appointment_data))
    return db_appointment

@router.get("/", response_model=List[schemas.AppointmentResponse])
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    patient_id: Optional[int] = Query(None),
    doctor_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Retrieves a list of appointments.
    Allows filtering by patient_id, clinic_id, or doctor_id.
    Requires 'appointments.read' permission.
    """
    service = AppointmentService(db)
    return service.get_appointments(
        skip=skip, 
        limit=limit,
        clinic_id=clinic_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
        status=status,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/check-availability", response_model=schemas.AppointmentAvailabilityResponse)
def check_time_slot_availability(
    clinic_id: int,
    doctor_id: int,
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Verifica la disponibilidad de un horario para agendar una cita.
    
    Args:
        clinic_id: ID de la clínica
        doctor_id: ID del doctor
        resource_id: ID del recurso (consultorio)
        start_time: Hora de inicio propuesta
        end_time: Hora de fin propuesta
        
    Returns:
        Un objeto indicando si el horario está disponible
    
    Requires 'appointments.read' permission.
    """
    try:
        service = AppointmentService(db)
        is_available = service.is_time_slot_available(
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time
        )
        
        return schemas.AppointmentAvailabilityResponse(
            is_available=is_available,
            message="El horario está disponible" if is_available else "El horario no está disponible"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar disponibilidad: {str(e)}"
        )

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Retrieves a single appointment by its ID.
    Requires 'appointments.read' permission.
    """
    service = AppointmentService(db)
    db_appointment = service.get_appointment(appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    return db_appointment

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.update"))
):
    """
    Updates an existing appointment by its ID.
    Requires 'appointments.update' permission.
    """
    service = AppointmentService(db)
    # Set updated_by_user_id from the current user
    appointment_data = appointment.dict()
    appointment_data["updated_by_user_id"] = current_user.id

    db_appointment = service.update_appointment(appointment_id, schemas.AppointmentUpdate(**appointment_data))
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.delete"))
):
    """
    Deletes an appointment by its ID (soft delete).
    Requires 'appointments.delete' permission.
    """
    service = AppointmentService(db)
    if not service.delete_appointment(appointment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

@router.post("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    cancellation_data: Optional[schemas.AppointmentCancellation] = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.cancel"))
):
    """
    Cancels an appointment by its ID.
    Optionally accepts a reason for cancellation.
    Requires 'appointments.cancel' permission.
    """
    service = AppointmentService(db)
    cancellation_reason = cancellation_data.reason if cancellation_data is not None else None
    if not service.cancel_appointment(appointment_id, cancellation_reason):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"message": "Appointment canceled successfully"}

@router.get("/check-availability", response_model=schemas.AppointmentAvailabilityResponse)
def check_time_slot_availability(
    clinic_id: int,
    doctor_id: int,
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("appointments.read"))
):
    """
    Verifica la disponibilidad de un horario para agendar una cita.
    
    Args:
        clinic_id: ID de la clínica
        doctor_id: ID del doctor
        resource_id: ID del recurso (consultorio)
        start_time: Hora de inicio propuesta
        end_time: Hora de fin propuesta
        
    Returns:
        Un objeto indicando si el horario está disponible
    
    Requires 'appointments.read' permission.
    """
    try:
        service = AppointmentService(db)
        is_available = service.is_time_slot_available(
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time
        )
        
        return schemas.AppointmentAvailabilityResponse(
            is_available=is_available,
            message="El horario está disponible" if is_available else "El horario no está disponible"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar disponibilidad: {str(e)}"
        )
