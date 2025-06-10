from app.data.repositories.appointment_repository import AppointmentRepository
from app.data.repositories.appointment_service_repository import AppointmentServiceRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

class AppointmentService:
    def __init__(self, db: Session):
        self.repository = AppointmentRepository(db)

    def create_appointment(self, appointment: schemas.AppointmentCreate) -> schemas.AppointmentInDB:
        return self.repository.create(appointment)

    def get_appointment(self, appointment_id: int) -> Optional[schemas.AppointmentInDB]:
        return self.repository.get_by_id(appointment_id)    
    
    def get_appointments(
        self, 
        skip: int = 0, 
        limit: int = 100,
        clinic_id: Optional[int] = None,
        patient_id: Optional[int] = None,
        doctor_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[schemas.AppointmentInDB]:
        # Si se proporcionan criterios de filtrado específicos, aplicarlos
        if clinic_id is not None:
            return self.repository.get_by_clinic_id(clinic_id, skip, limit)
        elif patient_id is not None:
            return self.repository.get_by_patient_id(patient_id, skip, limit)
        elif doctor_id is not None:
            return self.repository.get_by_doctor_id(doctor_id, skip, limit)
        elif status is not None:
            return self.repository.get_by_status(status, skip, limit)
        elif start_date is not None or end_date is not None:
            return self.repository.get_by_date_range(start_date, end_date, skip, limit)
        # Si no hay filtros específicos, devolver todas las citas
        return self.repository.get_all(skip, limit)

    def update_appointment(self, appointment_id: int, appointment: schemas.AppointmentUpdate) -> Optional[schemas.AppointmentInDB]:
        return self.repository.update(appointment_id, appointment)

    def delete_appointment(self, appointment_id: int) -> bool:
        return self.repository.delete(appointment_id)

    def get_appointments_by_patient(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[schemas.AppointmentInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)

    def get_appointments_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[schemas.AppointmentInDB]:
        return self.repository.get_by_clinic_id(clinic_id, skip, limit)

    def get_appointments_by_doctor(self, doctor_id: int, skip: int = 0, limit: int = 100) -> List[schemas.AppointmentInDB]:
        return self.repository.get_by_doctor_id(doctor_id, skip, limit)    
    
    def cancel_appointment(self, appointment_id: int, cancellation_reason: Optional[str] = None) -> bool:
        """
        Cancela una cita cambiando su estado a 'Cancelled'.
        
        Args:
            appointment_id: ID de la cita a cancelar
            cancellation_reason: Motivo opcional de la cancelación
            
        Returns:
            bool: True si la cita fue cancelada exitosamente, False si no se encontró la cita
        """
        appointment = self.repository.get_by_id(appointment_id)
        if not appointment:
            return False
            
        # Crear un objeto de actualización con el estado cancelado
        update_data = {
            "status": "Cancelled"
        }
        
        # Añadir la razón de cancelación si se proporciona
        if cancellation_reason:
            update_data["cancellation_reason"] = cancellation_reason
            
        # Actualizar la cita
        appointment_update = schemas.AppointmentUpdate(**update_data)
        self.repository.update(appointment_id, appointment_update)
        return True
