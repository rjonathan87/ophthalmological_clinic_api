from typing import List, Optional
from sqlalchemy.orm import Session
from app.data.repositories.patient_education_tracking_repository import PatientEducationTrackingRepository
from app.domain.schemas import (
    PatientEducationTrackingCreate,
    PatientEducationTrackingUpdate,
    PatientEducationTrackingInDB,
    PatientEducationTrackingResponse
)
from fastapi import HTTPException, status

class PatientEducationTrackingService:
    def __init__(self, db: Session):
        self.repository = PatientEducationTrackingRepository(db)

    def create_tracking(self, tracking: PatientEducationTrackingCreate, user_id: int) -> PatientEducationTrackingInDB:
        return self.repository.create(tracking, user_id)

    def get_tracking(self, tracking_id: int) -> Optional[PatientEducationTrackingInDB]:
        tracking = self.repository.get_by_id(tracking_id)
        if not tracking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient education tracking not found"
            )
        return tracking

    def get_patient_trackings(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[PatientEducationTrackingInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)

    def get_resource_trackings(self, resource_id: int, skip: int = 0, limit: int = 100) -> List[PatientEducationTrackingInDB]:
        return self.repository.get_by_resource_id(resource_id, skip, limit)

    def get_all_trackings(self, skip: int = 0, limit: int = 100) -> List[PatientEducationTrackingInDB]:
        return self.repository.get_all(skip, limit)

    def update_tracking(self, tracking_id: int, tracking: PatientEducationTrackingUpdate, user_id: int) -> PatientEducationTrackingInDB:
        updated_tracking = self.repository.update(tracking_id, tracking, user_id)
        if not updated_tracking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient education tracking not found"
            )
        return updated_tracking

    def delete_tracking(self, tracking_id: int) -> bool:
        return self.repository.soft_delete(tracking_id)
