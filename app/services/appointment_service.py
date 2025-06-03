from app.data.repositories.appointment_repository import AppointmentRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class AppointmentService:
    def __init__(self, db: Session):
        self.repository = AppointmentRepository(db)

    def create_appointment(self, appointment: schemas.AppointmentCreate) -> schemas.AppointmentInDB:
        return self.repository.create(appointment)

    def get_appointment(self, appointment_id: int) -> Optional[schemas.AppointmentInDB]:
        return self.repository.get_by_id(appointment_id)

    def get_appointments(self, skip: int = 0, limit: int = 100) -> List[schemas.AppointmentInDB]:
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
