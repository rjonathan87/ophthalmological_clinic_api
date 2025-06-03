from sqlalchemy.orm import Session
from app.domain import models, schemas
from typing import List, Optional

class AppointmentServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, appointment_service: schemas.AppointmentServiceCreate) -> models.AppointmentService:
        db_appointment_service = models.AppointmentService(**appointment_service.model_dump())
        self.db.add(db_appointment_service)
        self.db.commit()
        self.db.refresh(db_appointment_service)
        return db_appointment_service

    def get_by_ids(self, appointment_id: int, service_id: int) -> Optional[models.AppointmentService]:
        return self.db.query(models.AppointmentService).filter(
            models.AppointmentService.appointment_id == appointment_id,
            models.AppointmentService.service_id == service_id
        ).first()

    def get_by_appointment_id(self, appointment_id: int) -> List[models.AppointmentService]:
        return self.db.query(models.AppointmentService).filter(
            models.AppointmentService.appointment_id == appointment_id
        ).all()

    def get_by_service_id(self, service_id: int) -> List[models.AppointmentService]:
        return self.db.query(models.AppointmentService).filter(
            models.AppointmentService.service_id == service_id
        ).all()

    def delete(self, appointment_id: int, service_id: int) -> bool:
        db_appointment_service = self.get_by_ids(appointment_id, service_id)
        if db_appointment_service:
            self.db.delete(db_appointment_service)
            self.db.commit()
            return True
        return False
