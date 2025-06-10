from sqlalchemy.orm import Session
from app.domain import schemas
from typing import List, Optional
from datetime import datetime

from app.domain.models import Appointment

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, appointment: schemas.AppointmentCreate) -> Appointment:
        db_appointment = Appointment(**appointment.dict())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        return self.db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.deleted_at == None).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.deleted_at == None).offset(skip).limit(limit).all()

    def update(self, appointment_id: int, appointment: schemas.AppointmentUpdate) -> Optional[Appointment]:
        db_appointment = self.get_by_id(appointment_id)
        if db_appointment:
            for key, value in appointment.dict(exclude_unset=True).items():
                setattr(db_appointment, key, value)
            self.db.commit()
            self.db.refresh(db_appointment)
        return db_appointment

    def delete(self, appointment_id: int) -> bool:
        db_appointment = self.get_by_id(appointment_id)
        if db_appointment:
            db_appointment.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(db_appointment)
            return True
        return False

    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return self.db.query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_clinic_id(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return self.db.query(Appointment).filter(
            Appointment.clinic_id == clinic_id,
            Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_doctor_id(self, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return self.db.query(Appointment).filter(
            Appointment.primary_doctor_id == doctor_id,
            Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return self.db.query(Appointment).filter(
            Appointment.status == status,
            Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Appointment]:
        query = self.db.query(Appointment).filter(Appointment.deleted_at == None)
        
        if start_date:
            query = query.filter(Appointment.appointment_date >= start_date)
        
        if end_date:
            query = query.filter(Appointment.appointment_date <= end_date)
            
        return query.offset(skip).limit(limit).all()

    def find_overlapping_appointments(
        self, 
        clinic_id: int,
        doctor_id: int,
        resource_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Appointment]:
        """
        Encuentra citas que se solapen con el horario propuesto.
        
        Args:
            clinic_id: ID de la clínica
            doctor_id: ID del doctor
            resource_id: ID del recurso
            start_time: Hora de inicio propuesta
            end_time: Hora de fin propuesta
            
        Returns:
            List[Appointment]: Lista de citas que se solapan con el horario
        """
        try:
            from sqlalchemy import or_, and_
            
            query = self.db.query(Appointment).filter(
                Appointment.clinic_id == clinic_id,
                Appointment.primary_doctor_id == doctor_id,
                Appointment.resource_id == resource_id,
                Appointment.status.not_in(['Cancelled', 'NoShow']),
                Appointment.deleted_at == None,
                or_(
                    and_(Appointment.start_time <= end_time, Appointment.end_time >= start_time),
                    and_(Appointment.start_time >= start_time, Appointment.start_time < end_time),
                    and_(Appointment.end_time > start_time, Appointment.end_time <= end_time)
                )
            )
            
            return query.all()
        except Exception as e:
            # Registrar el error si hay un logger disponible
            raise Exception(f"Error al buscar citas solapadas: {str(e)}")