from sqlalchemy.orm import Session
from app.domain import models, schemas
from typing import List, Optional
from datetime import datetime

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, appointment: schemas.AppointmentCreate) -> models.Appointment:
        db_appointment = models.Appointment(**appointment.dict())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def get_by_id(self, appointment_id: int) -> Optional[models.Appointment]:
        return self.db.query(models.Appointment).filter(models.Appointment.id == appointment_id, models.Appointment.deleted_at == None).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
        return self.db.query(models.Appointment).filter(models.Appointment.deleted_at == None).offset(skip).limit(limit).all()

    def update(self, appointment_id: int, appointment: schemas.AppointmentUpdate) -> Optional[models.Appointment]:
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

    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
        return self.db.query(models.Appointment).filter(
            models.Appointment.patient_id == patient_id,
            models.Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_clinic_id(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
        return self.db.query(models.Appointment).filter(
            models.Appointment.clinic_id == clinic_id,
            models.Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_doctor_id(self, doctor_id: int, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
        return self.db.query(models.Appointment).filter(
            models.Appointment.primary_doctor_id == doctor_id,
            models.Appointment.deleted_at == None
        ).offset(skip).limit(limit).all()
