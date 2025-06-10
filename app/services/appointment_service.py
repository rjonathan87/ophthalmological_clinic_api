from app.data.repositories.appointment_repository import AppointmentRepository
from app.data.repositories.appointment_service_repository import AppointmentServiceRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

class AppointmentServiceError(Exception):
    """Custom exception for AppointmentService errors."""
    pass

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

    def is_time_slot_available(
        self,
        clinic_id: int,
        doctor_id: int,
        resource_id: int, 
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """
        Verifica si un horario está disponible para agendar una cita.
        
        Args:
            clinic_id: ID de la clínica
            doctor_id: ID del doctor 
            resource_id: ID del recurso (consultorio)
            start_time: Hora de inicio propuesta
            end_time: Hora de fin propuesta
            
        Returns:
            bool: True si el horario está disponible, False si ya existe una cita
        """
        try:
            overlapping_appointments = self.repository.find_overlapping_appointments(
                clinic_id=clinic_id,
                doctor_id=doctor_id,
                resource_id=resource_id,
                start_time=start_time,
                end_time=end_time
            )
            
            return len(overlapping_appointments) == 0
        except Exception as e:
            # Registrar el error si hay un logger disponible
            raise AppointmentServiceError(f"No se pudo verificar la disponibilidad del horario: {str(e)}")

    def find_alternative_slots(
        self,
        clinic_id: int,
        doctor_id: int,
        resource_id: int,
        start_time: datetime,
        end_time: datetime,
        num_alternatives: int = 3,
        days_range: int = 7,
        check_other_doctors: bool = True
    ) -> List[schemas.AppointmentAlternative]:
        """
        Busca horarios alternativos disponibles cuando el horario solicitado no está disponible.
        
        Args:
            clinic_id: ID de la clínica
            doctor_id: ID del doctor
            resource_id: ID del recurso (consultorio)
            start_time: Hora de inicio propuesta originalmente
            end_time: Hora de fin propuesta originalmente
            num_alternatives: Número de alternativas a sugerir
            days_range: Rango de días en el futuro para buscar alternativas
            check_other_doctors: Si se deben verificar otros médicos como alternativa
            
        Returns:
            List[schemas.AppointmentAlternative]: Lista de horarios alternativos disponibles
        """
        
        # Duración de la cita solicitada
        appointment_duration = end_time - start_time
        
        # Generamos alternativas para el mismo día
        alternatives = []
        
        # 1. Intentamos con horarios más tarde el mismo día
        current_day = start_time.date()
        current_time = start_time + timedelta(hours=1)  # Empezamos 1 hora después
        while current_time.date() == current_day and len(alternatives) < num_alternatives:
            alt_start = current_time
            alt_end = alt_start + appointment_duration
            
            # Verificamos si este horario está disponible
            if self.is_time_slot_available(clinic_id, doctor_id, resource_id, alt_start, alt_end):
                alternatives.append(schemas.AppointmentAlternative(
                    start_time=alt_start,
                    end_time=alt_end
                ))
            
            # Avanzamos 30 minutos para la siguiente verificación
            current_time += timedelta(minutes=30)
        
        # 2. Si no tenemos suficientes alternativas, buscamos en los próximos días
        if len(alternatives) < num_alternatives:
            for day_offset in range(1, days_range + 1):
                if len(alternatives) >= num_alternatives:
                    break
                    
                next_day = start_time.date() + timedelta(days=day_offset)
                
                # Horarios comunes para citas (9:00 AM a 5:00 PM)
                for hour in [9, 10, 11, 12, 14, 15, 16]:
                    if len(alternatives) >= num_alternatives:
                        break
                        
                    # Intentamos a la hora en punto y a la media hora
                    for minute in [0, 30]:
                        if len(alternatives) >= num_alternatives:
                            break
                            
                        alt_start = datetime.combine(next_day, datetime.min.time().replace(hour=hour, minute=minute))
                        alt_end = alt_start + appointment_duration
                        
                        # Verificamos disponibilidad
                        if self.is_time_slot_available(clinic_id, doctor_id, resource_id, alt_start, alt_end):
                            alternatives.append(schemas.AppointmentAlternative(
                                start_time=alt_start,
                                end_time=alt_end
                            ))
        
        # 3. Si check_other_doctors es True y aún no tenemos suficientes alternativas,
        # verificamos otros médicos para el horario original
        if check_other_doctors and len(alternatives) < num_alternatives:
            try:
                # Aquí necesitaríamos buscar otros médicos disponibles en la misma clínica
                # Esta es una versión simplificada, en un caso real se debería integrar
                # con el repositorio de usuarios/médicos de la clínica
                
                # Por simplicidad, asumimos que tenemos acceso a un servicio de usuarios
                # que puede darnos los médicos de una clínica
                from app.services.user_service import UserService
                user_service = UserService(self.repository.db)
                
                # Obtenemos los médicos de la clínica
                doctors = user_service.get_doctors_by_clinic(clinic_id)
                
                for doctor in doctors:
                    if doctor.id == doctor_id:  # Saltamos al médico original
                        continue
                        
                    if len(alternatives) >= num_alternatives:
                        break
                        
                    # Verificamos si este médico está disponible en el horario original
                    if self.is_time_slot_available(clinic_id, doctor.id, resource_id, start_time, end_time):
                        alternatives.append(schemas.AppointmentAlternative(
                            start_time=start_time,
                            end_time=end_time,
                            doctor_id=doctor.id,
                            doctor_name=f"{doctor.first_name} {doctor.last_name}"
                        ))
                    
                    # Si aún necesitamos más alternativas, verificamos horarios cercanos para este médico
                    if len(alternatives) < num_alternatives:
                        # Probamos algunas horas más tarde el mismo día
                        alt_time = start_time + timedelta(hours=1)
                        while alt_time.date() == start_time.date() and len(alternatives) < num_alternatives:
                            alt_end_time = alt_time + appointment_duration
                            if self.is_time_slot_available(clinic_id, doctor.id, resource_id, alt_time, alt_end_time):
                                alternatives.append(schemas.AppointmentAlternative(
                                    start_time=alt_time,
                                    end_time=alt_end_time,
                                    doctor_id=doctor.id,
                                    doctor_name=f"{doctor.first_name} {doctor.last_name}"
                                ))
                            alt_time += timedelta(minutes=30)
            except Exception as e:
                # Si hay algún error al buscar otros médicos, continuamos con lo que tenemos
                # En un entorno de producción, se debería registrar este error
                pass
        
        return alternatives