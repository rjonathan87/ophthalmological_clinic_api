from app.data.repositories.appointment_service_repository import AppointmentServiceRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class AppointmentServiceService:
    def __init__(self, db: Session):
        self.repository = AppointmentServiceRepository(db)

    def create_appointment_service(self, appointment_service: schemas.AppointmentServiceCreate) -> schemas.AppointmentServiceInDB:
        return self.repository.create(appointment_service)

    def get_appointment_service(self, appointment_id: int, service_id: int) -> Optional[schemas.AppointmentServiceInDB]:
        return self.repository.get_by_ids(appointment_id, service_id)

    def get_services_for_appointment(self, appointment_id: int) -> List[schemas.AppointmentServiceInDB]:
        return self.repository.get_by_appointment_id(appointment_id)

    def get_appointments_for_service(self, service_id: int) -> List[schemas.AppointmentServiceInDB]:
        return self.repository.get_by_service_id(service_id)

    def delete_appointment_service(self, appointment_id: int, service_id: int) -> bool:
        return self.repository.delete(appointment_id, service_id)
